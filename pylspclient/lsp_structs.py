import enum
from typing import Any, List, Optional, Type, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


def to_type(o: Any, new_type: Type[T]) -> T:
    """
    Helper funciton that receives an object or a dict and convert it to a new given type.

    :param object|dict o: The object to convert
    :param Type new_type: The type to convert to.
    """
    if new_type == type(o):
        return o
    else:
        return new_type(**o)


class Position(BaseModel):
    line: int
    character: int


class Range(BaseModel):
    start: Position
    end: Position


class Location(BaseModel):
    """
    Represents a location inside a resource, such as a line inside a text file.
    """

    uri: str
    range: Range


class LocationLink(BaseModel):
    """
    Represents a link between a source and a target location.
    """

    originSelectionRange: Range
    targetUri: str
    targetRange: Range
    targetSelectionRange: Range


class Diagnostic(BaseModel):
    range: Range
    severity: int
    code: str
    source: str
    mesasge: str
    relatedInformation: List[Any]


class DiagnosticSeverity(object):
    Error = 1
    Warning = 2  # TODO: warning is known in python
    Information = 3
    Hint = 4


class DiagnosticRelatedInformation(BaseModel):
    location: Location
    message: str


class Command(BaseModel):
    title: str
    command: str
    arguments: List[Any]


class TextDocumentItem(BaseModel):
    """
    An item to transfer a text document from the client to the server.
    """

    uri: str
    languageId: str
    version: int
    text: str


class TextDocumentIdentifier(BaseModel):
    """
    Text documents are identified using a URI. On the protocol level, URIs are passed as strings.
    """

    uri: str


class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """
    An identifier to denote a specific version of a text document.
    """

    version: int


class TextDocumentContentChangeEvent(BaseModel):
    """
    An event describing a change to a text document. If range and rangeLength are omitted
    the new text is considered to be the full content of the document.
    """

    range: Range
    rangeLength: int
    text: str


class TextDocumentPositionParams(BaseModel):
    """
    A parameter literal used in requests to pass a text document and a position inside that document.
    """

    textDocument: TextDocumentIdentifier
    position: Position


class LANGUAGE_IDENTIFIER(object):
    BAT = "bat"
    BIBTEX = "bibtex"
    CLOJURE = "clojure"
    COFFESCRIPT = "coffeescript"
    C = "c"
    CPP = "cpp"
    CSHARP = "csharp"
    CSS = "css"
    DIFF = "diff"
    DOCKERFILE = "dockerfile"
    FSHARP = "fsharp"
    GIT_COMMIT = "git-commit"
    GIT_REBASE = "git-rebase"
    GO = "go"
    GROOVY = "groovy"
    HANDLEBARS = "handlebars"
    HTML = "html"
    INI = "ini"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    JSON = "json"
    LATEX = "latex"
    LESS = "less"
    LUA = "lua"
    MAKEFILE = "makefile"
    MARKDOWN = "markdown"
    OBJECTIVE_C = "objective-c"
    OBJECTIVE_CPP = "objective-cpp"
    Perl = "perl"
    PHP = "php"
    POWERSHELL = "powershell"
    PUG = "jade"
    PYTHON = "python"
    R = "r"
    RAZOR = "razor"
    RUBY = "ruby"
    RUST = "rust"
    SASS = "sass"
    SCSS = "scss"
    ShaderLab = "shaderlab"
    SHELL_SCRIPT = "shellscript"
    SQL = "sql"
    SWIFT = "swift"
    TYPE_SCRIPT = "typescript"
    TEX = "tex"
    VB = "vb"
    XML = "xml"
    XSL = "xsl"
    YAML = "yaml"


class SymbolKind(enum.Enum):
    File = 1
    Module = 2
    Namespace = 3
    Package = 4
    Class = 5
    Method = 6
    Property = 7
    Field = 8
    Constructor = 9
    Enum = 10
    Interface = 11
    Function = 12
    Variable = 13
    Constant = 14
    String = 15
    Number = 16
    Boolean = 17
    Array = 18
    Object = 19
    Key = 20
    Null = 21
    EnumMember = 22
    Struct = 23
    Event = 24
    Operator = 25
    TypeParameter = 26


class SymbolInformation(BaseModel):
    """
    Represents information about programming constructs like variables, classes, interfaces etc.
    """

    name: str
    kind: SymbolKind
    location: Location
    containerName: Optional[str] = None
    deprecated: bool = False


class DocumnetSymbol(BaseModel):
    """
    Represents information about programming constructs like variables, classes, interfaces etc.
    """

    name: str
    kind: SymbolKind
    range: Range
    selectionRange: Range
    children: List["DocumnetSymbol"] = Field(default_factory=list)
    containerName: Optional[str] = None
    deprecated: bool = False


class ParameterInformation(BaseModel):
    """
    Represents a parameter of a callable-signature. A parameter can
    have a label and a doc-comment.
    """

    label: str
    documentation: str = Field("")


class SignatureInformation(BaseModel):
    """
    Represents the signature of something callable. A signature
    can have a label, like a function-name, a doc-comment, and
    a set of parameters.
    """

    label: str
    documentation: str = Field("")
    parameters: List[ParameterInformation] = Field(default_factory=list)


class SignatureHelp(BaseModel):
    """
    Signature help represents the signature of something
    callable. There can be multiple signature but only one
    active and only one active parameter.
    """

    signatures: List[SignatureInformation]
    activeSignature: int = Field(0)
    activeParameter: int = Field(0)


class CompletionTriggerKind(enum.Enum):
    Invoked = 1
    TriggerCharacter = 2
    TriggerForIncompleteCompletions = 3


class CompletionContext(BaseModel):
    """
    Contains additional information about the context in which a completion request is triggered.
    """

    triggerKind: CompletionTriggerKind
    triggerCharacter: Optional[str] = Field(None)


class ReferenceContext(BaseModel):
    includeDeclaration: bool = Field(False)


class TextEdit(BaseModel):
    """
    A textual edit applicable to a text document.
    """

    range: Range
    newText: str


class InsertTextFormat(enum.Enum):
    PlainText = 1
    Snippet = 2


class CompletionItem(BaseModel):
    """ """

    label: str
    kind: Optional[int] = None
    detail: Optional[str] = None
    documentation: Optional[str] = None
    deprecated: Optional[bool] = None
    presented: Optional[bool] = None
    sortText: Optional[str] = None
    filterText: Optional[str] = None
    insertText: Optional[str] = None
    insertTextFormat: Optional[InsertTextFormat] = None
    textEdit: Optional[TextEdit] = None
    additionalTextEdits: Optional[TextEdit] = None
    commitCharacters: Optional[str] = None
    command: Optional[Command] = None
    data: Optional[Any] = None
    score: float = 0.0


class CompletionItemKind(enum.Enum):
    Text = 1
    Method = 2
    Function = 3
    Constructor = 4
    Field = 5
    Variable = 6
    Class = 7
    Interface = 8
    Module = 9
    Property = 10
    Unit = 11
    Value = 12
    Enum = 13
    Keyword = 14
    Snippet = 15
    Color = 16
    File = 17
    Reference = 18
    Folder = 19
    EnumMember = 20
    Constant = 21
    Struct = 22
    Event = 23
    Operator = 24
    TypeParameter = 25


class CompletionList(BaseModel):
    """
    Represents a collection of [completion items](#CompletionItem) to be presented in the editor.
    """

    isIncomplete: bool
    items: List[CompletionItem]


class ErrorCodes(enum.Enum):
    # Defined by JSON RPC
    ParseError = -32700
    InvalidRequest = -32600
    MethodNotFound = -32601
    InvalidParams = -32602
    InternalError = -32603
    serverErrorStart = -32099
    serverErrorEnd = -32000
    ServerNotInitialized = -32002
    UnknownErrorCode = -32001

    # Defined by the protocol.
    RequestCancelled = -32800
    ContentModified = -32801


class ResponseError(Exception):
    def __init__(self, code: ErrorCodes, message: str, data: Optional[Any] = None):
        self.code = code
        self.message = message
        if data:
            self.data = data
