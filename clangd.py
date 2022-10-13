from time import sleep
import pylspclient
import subprocess
import threading
import argparse
from pylspclient.lsp_client import LspClient

from pylspclient.lsp_structs import DocumnetSymbol, SymbolInformation

PHP_LANGUAGE_SERVER = "/home/a-ohta/php-language-server"


class ReadPipe(threading.Thread):
    def __init__(self, pipe):
        threading.Thread.__init__(self)
        self.pipe = pipe

    def run(self):
        line = self.pipe.readline().decode("utf-8")
        while line:
            print(line)
            line = self.pipe.readline().decode("utf-8")


def get_reference(lsp_client: LspClient, symbol: DocumnetSymbol):
    line = symbol.range.start.line
    character = symbol.range.start.character
    locations = lsp_client.references(
        pylspclient.lsp_structs.TextDocumentIdentifier(uri=uri),
        pylspclient.lsp_structs.Position(line=line, character=character),
        pylspclient.lsp_structs.ReferenceContext(),
    )
    print(
        f"{symbol.name}, {symbol.range.start.line}, {symbol.range.start.character}, {[location.dict() for location in locations]}"
    )
    for child in symbol.children:
        get_reference(lsp_client=lsp_client, symbol=child)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="pylspclient example with clangd")
    parser.add_argument(
        "clangd_path",
        type=str,
        default="/usr/bin/clangd-6.0",
        help="the clangd path",
        nargs="?",
    )
    args = parser.parse_args()
    intelephense = ["intelephense", "--stdio"]
    phpls = [
        "php",
        PHP_LANGUAGE_SERVER
        + "/vendor/felixfbecker/language-server/bin/php-language-server.php",
    ]
    p = subprocess.Popen(
        intelephense,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    read_pipe = ReadPipe(p.stderr)
    read_pipe.start()
    json_rpc_endpoint = pylspclient.JsonRpcEndpoint(p.stdin, p.stdout)
    # To work with socket: sock_fd = sock.makefile()
    lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint, timeout=99999999)

    lsp_client = pylspclient.LspClient(lsp_endpoint)
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
    root_uri = "file:///home/a-ohta/Buzz/"
    workspace_folders = [{"name": "python-lsp", "uri": root_uri}]
    print("before initialized")
    print(
        lsp_client.initialize(
            processId=p.pid,
            rootPath=None,
            rootUri=root_uri,
            initializationOptions=None,
            capabilities=capabilities,
            trace="off",
            workspaceFolders=workspace_folders,
        )
    )
    print("initializing...")
    print(lsp_client.initialized())
    print("after initialized")
    sleep(5)

    file_path = "/home/a-ohta/Buzz/lib/Client/Curl.php"
    uri = "file://" + file_path
    text = open(file_path, "r").read()
    languageId = pylspclient.lsp_structs.LANGUAGE_IDENTIFIER.PHP
    version = 1
    documentItem = pylspclient.lsp_structs.TextDocumentItem(
        uri=uri, languageId=languageId, version=version, text=text
    )
    lsp_client.didOpen(documentItem)
    try:
        symbols = lsp_client.documentSymbol(documentItem)
        print(f"Get references for all symbols in file: {documentItem.uri}.")
        for symbol in symbols:
            if isinstance(symbol, SymbolInformation):
                print(
                    f"{symbol.name}: {symbol.location.range.start.line}, {symbol.location.range.start.character}"
                )
                line = symbol.location.range.start.line
                character = symbol.location.range.start.character
            else:
                get_reference(lsp_client, symbol)
    except pylspclient.lsp_structs.ResponseError as e:
        # documentSymbol is supported from version 8.
        print(e)
        print("Failed to document symbols")

    lsp_client.shutdown()
    lsp_client.exit()
