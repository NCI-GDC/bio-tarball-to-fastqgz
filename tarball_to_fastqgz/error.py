class Error(Exception):
    """Base class"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class NoStrategyError(Error):
    """No strategy found to unpack and stage data."""

    pass


class UndefinedTarType(Error):
    """Tar type undefined"""

    def __init__(self, value: str) -> None:
        super().__init__(f"Unexpected tar type: {value}")


class UndefinedFastqType(Error):
    """unexpected FASTQ Type"""

    def __init__(self, value: str) -> None:
        super().__init__(f"Unexpected fastq type: {value}")


class FqNumberOutOfBounds(Error):
    """Number of FASTQ Files out of bounds"""

    def __init__(self, value: int) -> None:
        super().__init__(f"Unexpected number of fastq files: {value}")


class UnexpectedPEType(Error):
    """Unexpected value for PE"""

    def __init__(self, value: str) -> None:
        super().__init__(f"Unexpected value for PE: {value}")
