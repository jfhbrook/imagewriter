# API Documentation

This section documents the API in the `imagewriter` Python module. This documentation is dense, but comprehensively covers the semantics of the ImageWriter II.

## The Basics

* [imagewriter.base](./base.md) - base abstractions

## Connection Management

* [imagewriter.serial](./serial.md) - low level serial connectivity
* [imagewriter.connection](./connection.md) - high level connection management

## Commands

* [imagewriter.encoding](./encoding.md) - the `Command` class and all its friends

## Document Rendering

* [imagewriter.document](./document.md) - a document object model inspired by `pandoc`
* [imagewriter.render](./render.md) - render rich text, documents specified by a DOM, or text documents in a format supported by Pandoc

## Applications and Interfaces

* [imagewriter.container](./container.md) - a dependency injection container for common objects
* [imagewriter.widgets](./widgets.md) - an IPyWidget control panel for use with Jupyter

## Testing and Debugging

* [imagewriter.debug](./debug.md) - debugging tools, particularly for serial state
* [imagewriter.test](./test.md) - Test pages and memory testing
