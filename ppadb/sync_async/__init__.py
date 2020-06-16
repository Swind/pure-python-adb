import struct
import os

from ppadb.protocol import Protocol
from ppadb.sync.stats import S_IFREG
from ppadb.utils.logger import AdbLogging

logger = AdbLogging.get_logger(__name__)


class SyncAsync:
    DATA_MAX_LENGTH = 65536

    def __init__(self, connection):
        self.connection = connection

    async def push(self, src, dest, mode, progress=None):
        """Push from local path |src| to |dest| on device.
        :param progress: callback, called with (filename, total_size, sent_size)
        """
        if not os.path.exists(src):
            raise FileNotFoundError("Can't find the source file {}".format(src))

        stat = os.stat(src)

        timestamp = int(stat.st_mtime)

        total_size = os.path.getsize(src)
        sent_size = 0

        # SEND
        mode = mode | S_IFREG
        args = "{dest},{mode}".format(dest=dest, mode=mode)
        await self._send_str(Protocol.SEND, args)

        # DATA
        with open(src, 'rb') as stream:
            while True:
                chunk = stream.read(self.DATA_MAX_LENGTH)
                if not chunk:
                    break

                sent_size += len(chunk)
                await self._send_length(Protocol.DATA, len(chunk))
                await self.connection.write(chunk)

                if progress is not None:
                    progress(src, total_size, sent_size)

        # DONE
        await self._send_length(Protocol.DONE, timestamp)
        await self.connection._check_status()

    async def pull(self, src, dest):
        # RECV
        await self._send_str(Protocol.RECV, src)

        # DATA
        with open(dest, 'wb') as stream:
            while True:
                flag = (await self.connection.read(4)).decode('utf-8')

                if flag == Protocol.DATA:
                    data = await self._read_data()
                    stream.write(data)
                    continue

                if flag == Protocol.DONE:
                    await self.connection.read(4)
                    return

                if flag == Protocol.FAIL:
                    return (await self._read_data()).decode('utf-8')

    @staticmethod
    def _integer(little_endian):
        return struct.unpack("<I", little_endian)

    @staticmethod
    def _little_endian(n):
        return struct.pack('<I', n)

    async def _read_data(self):
        length = self._integer(await self.connection.read(4))[0]
        data = bytearray()
        while len(data) < length:
            data += await self.connection.read(length - len(data))
        return data

    async def _send_length(self, cmd, length):
        le_len = self._little_endian(length)
        data = cmd.encode() + le_len

        logger.debug("Send length: {}".format(data))
        await self.connection.write(data)

    async def _send_str(self, cmd, args):
        """
        Format:
            {Command}{args length(little endian)}{str}
        Length:
            {4}{4}{str length}
        """
        logger.debug("{} {}".format(cmd, args))
        args = args.encode('utf-8')

        le_args_len = self._little_endian(len(args))
        data = cmd.encode() + le_args_len + args
        logger.debug("Send string: {}".format(data))
        await self.connection.write(data)
