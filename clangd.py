import subprocess
import threading
from pathlib import Path
from sys import stderr
from time import sleep
from typing import IO, Any, Dict, List, Set, Union

import click

import pylspclient
from pylspclient.lsp_client import LspClient
from pylspclient.lsp_structs import (
    DocumnetSymbol,
    Location,
    SymbolInformation,
    TextDocumentItem,
)

PHP_LANGUAGE_SERVER = "/home/a-ohta/php-language-server"
## root directory for diagnose
ROOT_DIR = "/home/a-ohta/Buzz/"
## target file for get references
FILE_PATH = "/home/a-ohta/Buzz/lib/Client/Curl.php"

FILE_PARSE_TIMEOUT_SEC = 30
_DONE_FILES: Set[str] = set()


class ReadPipe(threading.Thread):
    def __init__(self, pipe: IO[bytes]):
        threading.Thread.__init__(self)
        self.pipe = pipe

    def run(self):
        line = self.pipe.readline().decode("utf-8")
        while line:
            print(line, file=stderr)
            line = self.pipe.readline().decode("utf-8")


def print_reference(
    uri: str,
    line: int,
    character: int,
    name: str,
    locations: Union[List[Location], Location],
    documents: Dict[str, TextDocumentItem],
):
    _locations: List[Location] = []
    if isinstance(locations, Location):
        _locations.append(locations)
    else:
        _locations = locations
    if not _locations:
        print(f'"{uri}", {line}, {character}, "{name}"')
    for location in _locations:
        document = documents[location.uri[len("file://") :]]
        loc_line = location.range.start.line
        loc_chracter = location.range.start.character
        line_str = document.text.splitlines()[loc_line]
        print(
            f'"{uri}", {line}, {character}, "{name}", "{location.uri}", {loc_line}, {loc_chracter}, `{line_str}`'
        )


def get_reference(
    lsp_client: LspClient,
    symbol: Union[DocumnetSymbol, SymbolInformation],
    uri: str,
    documents: Dict[str, TextDocumentItem],
):
    if isinstance(symbol, DocumnetSymbol):
        line = symbol.selectionRange.start.line
        character = symbol.selectionRange.start.character
        locations = lsp_client.references(
            pylspclient.lsp_structs.TextDocumentIdentifier(uri=uri),
            pylspclient.lsp_structs.Position(line=line, character=character),
            pylspclient.lsp_structs.ReferenceContext(includeDeclaration=True),
        )
        print_reference(uri, line, character, symbol.name, locations, documents)
        for child in symbol.children:
            get_reference(
                lsp_client=lsp_client, symbol=child, uri=uri, documents=documents
            )
    else:
        line = symbol.location.range.start.line + 3
        character = symbol.location.range.start.character
        locations = lsp_client.references(
            pylspclient.lsp_structs.TextDocumentIdentifier(uri=uri),
            pylspclient.lsp_structs.Position(line=line, character=character),
            pylspclient.lsp_structs.ReferenceContext(includeDeclaration=True),
        )
        print_reference(uri, line, character, symbol.name, locations, documents)


def open_all_source_files(lsp_client: LspClient, root_dir: Path):
    opened_files: Dict[str, TextDocumentItem] = {}
    for file in root_dir.glob("**/*.php"):
        file_path = str(file.absolute())
        uri = "file://" + file_path
        text = open(file_path, "r").read()
        languageId = pylspclient.lsp_structs.LANGUAGE_IDENTIFIER.PHP
        version = 1
        documentItem = pylspclient.lsp_structs.TextDocumentItem(
            uri=uri, languageId=languageId, version=version, text=text
        )
        lsp_client.didOpen(documentItem)
        opened_files[file_path] = documentItem
    return opened_files


def start_communication(lsp_client: LspClient, server_p: subprocess.Popen[bytes]):
    capabilities = {
        "textDocument": {
            "codeAction": {"dynamicRegistration": True},
            "codeLens": {"dynamicRegistration": True},
            "colorProvider": {"dynamicRegistration": True},
            "completion": {
                "completionItem": {
                    "commitCharactersSupport": True,
                    "documentationFormat": ["markdown", "plaintext"],
                    "snippetSupport": True,
                },
                "completionItemKind": {
                    "valueSet": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                    ]
                },
                "contextSupport": True,
                "dynamicRegistration": True,
            },
            "definition": {"dynamicRegistration": True},
            "documentHighlight": {"dynamicRegistration": True},
            "documentLink": {"dynamicRegistration": True},
            "documentSymbol": {
                "dynamicRegistration": True,
                "symbolKind": {
                    "valueSet": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                    ]
                },
                "hierarchicalDocumentSymbolSupport": True,
            },
            "formatting": {"dynamicRegistration": True},
            "hover": {
                "contentFormat": ["markdown", "plaintext"],
                "dynamicRegistration": True,
            },
            "implementation": {"dynamicRegistration": True},
            "onTypeFormatting": {"dynamicRegistration": True},
            "publishDiagnostics": {"relatedInformation": True},
            "rangeFormatting": {"dynamicRegistration": True},
            "references": {"dynamicRegistration": True},
            "rename": {"dynamicRegistration": True},
            "signatureHelp": {
                "dynamicRegistration": True,
                "signatureInformation": {
                    "documentationFormat": ["markdown", "plaintext"]
                },
            },
            "synchronization": {
                "didSave": True,
                "dynamicRegistration": True,
                "willSave": True,
                "willSaveWaitUntil": True,
            },
            "typeDefinition": {"dynamicRegistration": True},
        },
        "workspace": {
            "references": {"dynamicRegistration": True},
            "applyEdit": True,
            "configuration": True,
            "didChangeConfiguration": {"dynamicRegistration": True},
            "didChangeWatchedFiles": {"dynamicRegistration": True},
            "executeCommand": {"dynamicRegistration": True},
            "symbol": {
                "dynamicRegistration": True,
                "symbolKind": {
                    "valueSet": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                    ]
                },
            },
            "workspaceEdit": {"documentChanges": True},
            "workspaceFolders": True,
        },
    }
    root_uri = f"file:/{ROOT_DIR}"
    workspace_folders = [{"name": "python-lsp", "uri": root_uri}]
    print("before initialized", file=stderr)
    print(
        lsp_client.initialize(
            processId=server_p.pid,
            rootPath=None,
            rootUri=root_uri,
            initializationOptions=None,
            capabilities=capabilities,
            trace="verbose",
            workspaceFolders=workspace_folders,
        ),
        file=stderr,
    )
    print("initializing...", file=stderr)
    print(lsp_client.initialized(), file=stderr)
    print("after initialized", file=stderr)
    documents = open_all_source_files(lsp_client=lsp_client, root_dir=Path(ROOT_DIR))
    files = set([document.uri for _, document in documents.items()])
    for _ in range(FILE_PARSE_TIMEOUT_SEC):
        if _DONE_FILES == files:
            break
        sleep(1)
    else:
        print("file parse timeout", file=stderr)
        return

    documentItem = documents[FILE_PATH]
    try:
        symbols = lsp_client.documentSymbol(documentItem)
        print(
            f"Get references for all symbols in file: {documentItem.uri}.", file=stderr
        )
        for symbol in symbols:
            get_reference(lsp_client, symbol, documentItem.uri, documents)
    except pylspclient.lsp_structs.ResponseError as e:
        # documentSymbol is supported from version 8.
        print(e, file=stderr)
        print("Failed to document symbols", file=stderr)


def publishDiagnostics(arg: Dict[str, Any]):
    uri = arg["uri"]
    _DONE_FILES.add(uri)
    print(f"Parse end: {uri}", file=stderr)


@click.command()
@click.argument("server", type=click.Choice(["phpls", "intelephense"]))
def main(server: str):
    intelephense = ["intelephense", "--stdio"]
    phpls = [
        "php",
        PHP_LANGUAGE_SERVER
        + "/vendor/felixfbecker/language-server/bin/php-language-server.php",
    ]
    p = subprocess.Popen(
        phpls if server == "phpls" else intelephense,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert p.stderr and p.stdin and p.stdout
    read_pipe = ReadPipe(p.stderr)
    read_pipe.start()
    json_rpc_endpoint = pylspclient.JsonRpcEndpoint(p.stdin, p.stdout)
    # To work with socket: sock_fd = sock.makefile()
    lsp_endpoint = pylspclient.LspEndpoint(
        json_rpc_endpoint,
        timeout=99999999,
        notify_callbacks={"textDocument/publishDiagnostics": publishDiagnostics},
    )

    lsp_client = pylspclient.LspClient(lsp_endpoint)
    try:
        start_communication(lsp_client=lsp_client, server_p=p)
    finally:
        lsp_client.shutdown()
        lsp_client.exit()


if __name__ == "__main__":
    main()
