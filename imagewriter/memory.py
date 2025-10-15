KILOBYTE = 1024


def print_buffer_size(expansion: bool = False) -> int:
    """
    The expected print buffer size.

    By default, the ImageWriter II has 2K of memory; with the 32K memory
    expansion, 32KB.

    For now, this memory is assumed to be completely available for buffered
    commands. This may be disproven with experimentation.
    """

    if expansion:
        return 32 * KILOBYTE
    return 2 * KILOBYTE
