
from chromatica import logger
from chromatica.util import load_external_module

load_external_module(__file__, "")
from clang import cindex

log = logger.logging.getLogger("chromatica")

class bcolors:
    HEADER = '\033[0;35;38m'
    OKBLUE = '\033[0;34;38m'
    OKGREEN = '\033[0;32;38m'
    WARNING = '\033[0;31;38m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[0;33;38m'
    UNDERLINE = '\033[0;36;38m'

def get_cursor(tu, filename, row, col):
    return cindex.Cursor.from_location(tu, \
        cindex.SourceLocation.from_position(tu, tu.get_file(filename), row, col))

def get_symbol(cursor):
    """docstring for get_symbol"""
    if cursor.kind == cindex.CursorKind.MACRO_DEFINITION:
        return cursor

    symbol = cursor.get_definition()
    if not symbol:
        symbol = cursor.referenced

    if not symbol:
        return None

    if symbol.kind == cindex.CursorKind.CONSTRUCTOR \
            or symbol.kind == cindex.CursorKind.DESTRUCTOR:
        symbol = symbol.semantic_parent

    return symbol

def get_symbol_from_loc(tu, filename, row, col):
    """docstring for get_symbol_from_loc"""
    cursor = get_cursor(tu, filename, row, col)

    if not cursor:
        return None
    tokens = cursor.get_tokens()
    for token in tokens:
        # if token.kind.value == 2 \
        #         and row == token.location.line \
        if row == token.location.line \
                and token.location.column <= col \
                and col < token.location.column + len(token.spelling):
            symbol = get_symbol(cursor)
            if symbol and symbol.spelling == token.spelling:
                return symbol
    return None

LITERAL_GROUP = {
    cindex.CursorKind.INTEGER_LITERAL: "Number",
    cindex.CursorKind.FLOATING_LITERAL: "Float",
    cindex.CursorKind.IMAGINARY_LITERAL: "Number",
    cindex.CursorKind.STRING_LITERAL: None,
    cindex.CursorKind.CHARACTER_LITERAL: "Character",
    cindex.CursorKind.OBJC_STRING_LITERAL: None,
}

TYPE_GROUP = {
    cindex.TypeKind.UNEXPOSED: "Variable",
    cindex.TypeKind.VOID: "Variable",
    cindex.TypeKind.BOOL: "Variable",
    cindex.TypeKind.CHAR_U: "Variable",
    cindex.TypeKind.UCHAR: "Variable",
    cindex.TypeKind.CHAR16: "Variable",
    cindex.TypeKind.CHAR32: "Variable",
    cindex.TypeKind.USHORT: "Variable",
    cindex.TypeKind.UINT: "Variable",
    cindex.TypeKind.ULONG: "Variable",
    cindex.TypeKind.ULONGLONG: "Variable",
    cindex.TypeKind.UINT128: "Variable",
    cindex.TypeKind.CHAR_S: "Variable",
    cindex.TypeKind.SCHAR: "Variable",
    cindex.TypeKind.WCHAR: "Variable",
    cindex.TypeKind.SHORT: "Variable",
    cindex.TypeKind.INT: "Variable",
    cindex.TypeKind.LONG: "Variable",
    cindex.TypeKind.LONGLONG: "Variable",
    cindex.TypeKind.INT128: "Variable",
    cindex.TypeKind.FLOAT: "Variable",
    cindex.TypeKind.DOUBLE: "Variable",
    cindex.TypeKind.LONGDOUBLE: "Variable",
    cindex.TypeKind.NULLPTR: "Variable",
    cindex.TypeKind.OVERLOAD: "Variable",
    cindex.TypeKind.DEPENDENT: "Variable",
    cindex.TypeKind.OBJCID: "Variable",
    cindex.TypeKind.OBJCCLASS: "Variable",
    cindex.TypeKind.OBJCSEL: "Variable",
    cindex.TypeKind.COMPLEX: "Variable",
    cindex.TypeKind.POINTER: "Variable",
    cindex.TypeKind.BLOCKPOINTER: "Variable",
    cindex.TypeKind.LVALUEREFERENCE: "Variable",
    cindex.TypeKind.RVALUEREFERENCE: "Variable",
    cindex.TypeKind.RECORD: "Variable",
    cindex.TypeKind.TYPEDEF: "Variable",
    cindex.TypeKind.OBJCINTERFACE: "Variable",
    cindex.TypeKind.OBJCOBJECTPOINTER: "Variable",
    cindex.TypeKind.CONSTANTARRAY: "Variable",
    cindex.TypeKind.VECTOR: "Variable",
    cindex.TypeKind.INCOMPLETEARRAY: "Variable",
    cindex.TypeKind.VARIABLEARRAY: "Variable",
    cindex.TypeKind.DEPENDENTSIZEDARRAY: "Variable",
    cindex.TypeKind.AUTO: "Variable",
    cindex.TypeKind.MEMBERPOINTER: "Member",
    cindex.TypeKind.ENUM: "EnumConstant",
    cindex.TypeKind.FUNCTIONNOPROTO: "Function",
    cindex.TypeKind.FUNCTIONPROTO: "Function"
}

SYNTAX_GROUP = {
# Declarations
    cindex.CursorKind.UNEXPOSED_DECL: None,
    cindex.CursorKind.STRUCT_DECL: "chromaticaStructDecl",
    cindex.CursorKind.UNION_DECL: "chromaticaUnionDecl",
    cindex.CursorKind.CLASS_DECL: "chromaticaClassDecl",
    cindex.CursorKind.ENUM_DECL: "chromaticaEnumDecl",
    cindex.CursorKind.FIELD_DECL: "chromaticaFieldDecl",
    cindex.CursorKind.ENUM_CONSTANT_DECL: "chromaticaEnumConstantDecl",
    cindex.CursorKind.FUNCTION_DECL: "chromaticaFunctionDecl",
    cindex.CursorKind.VAR_DECL: "chromaticaVarDecl",
    cindex.CursorKind.PARM_DECL: "chromaticaParmDecl",
    cindex.CursorKind.OBJC_INTERFACE_DECL: "chromaticaObjCInterfaceDecl",
    cindex.CursorKind.OBJC_CATEGORY_DECL: "chromaticaObjCCategoryDecl",
    cindex.CursorKind.OBJC_PROTOCOL_DECL: "chromaticaObjCProtocolDecl",
    cindex.CursorKind.OBJC_PROPERTY_DECL: "chromaticaObjCPropertyDecl",
    cindex.CursorKind.OBJC_IVAR_DECL: "chromaticaObjCIvarDecl",
    cindex.CursorKind.OBJC_INSTANCE_METHOD_DECL: "chromaticaObjCInstanceMethodDecl",
    cindex.CursorKind.OBJC_CLASS_METHOD_DECL: "chromaticaObjCClassMethodDecl",
    cindex.CursorKind.OBJC_IMPLEMENTATION_DECL: "chromaticaObjCImplementationDecl",
    cindex.CursorKind.OBJC_CATEGORY_IMPL_DECL: "chromaticaObjCCategoryImplDecl",
    cindex.CursorKind.TYPEDEF_DECL: "chromaticaTypedefDecl",
    cindex.CursorKind.CXX_METHOD: "chromaticaFunctionDecl",
    cindex.CursorKind.NAMESPACE: "chromaticaNamespace",
    cindex.CursorKind.LINKAGE_SPEC: "chromaticaLinkageSpec",
    cindex.CursorKind.CONSTRUCTOR: "chromaticaFunctionDecl",
    cindex.CursorKind.DESTRUCTOR: "chromaticaFunctionDecl",
    cindex.CursorKind.CONVERSION_FUNCTION: "chromaticaConversionFunction",
    cindex.CursorKind.TEMPLATE_TYPE_PARAMETER: "chromaticaTemplateTypeParameter",
    cindex.CursorKind.TEMPLATE_NON_TYPE_PARAMETER: "chromaticaTemplateNoneTypeParameter",
    cindex.CursorKind.TEMPLATE_TEMPLATE_PARAMETER: "chromaticaTemplateTemplateParameter",
    cindex.CursorKind.FUNCTION_TEMPLATE: "chromaticaFunctionDecl",
    cindex.CursorKind.CLASS_TEMPLATE: "chromaticaClassDecl",
    cindex.CursorKind.CLASS_TEMPLATE_PARTIAL_SPECIALIZATION: "chromaticaClassTemplatePartialSpecialization",
    cindex.CursorKind.NAMESPACE_ALIAS: "chromaticaNamespaceAlias",
    cindex.CursorKind.USING_DIRECTIVE: "chromaticaUsingDirective",
    cindex.CursorKind.USING_DECLARATION: "chromaticaUsingDeclaration",
    cindex.CursorKind.TYPE_ALIAS_DECL: "chromaticaTypeAliasDecl",
    cindex.CursorKind.OBJC_SYNTHESIZE_DECL: "chromaticaObjCSynthesizeDecl",
    cindex.CursorKind.OBJC_DYNAMIC_DECL: "chromaticaObjCDynamicDecl",
    cindex.CursorKind.CXX_ACCESS_SPEC_DECL: "chromaticaCXXAccessSpecifier",
# References
    cindex.CursorKind.OBJC_SUPER_CLASS_REF: "chromaticaObjCSuperClassRef",
    cindex.CursorKind.OBJC_PROTOCOL_REF: "chromaticaObjCProtocolRef",
    cindex.CursorKind.OBJC_CLASS_REF: "chromaticaObjCClassRef",
    cindex.CursorKind.TYPE_REF: "chromaticaTypeRef",  # class ref
    cindex.CursorKind.CXX_BASE_SPECIFIER: "chromaticaCXXBaseSpecifier",
    cindex.CursorKind.TEMPLATE_REF: "chromaticaTemplateRef",  # template class ref
    cindex.CursorKind.NAMESPACE_REF: "chromaticaNamespaceRef",  # namespace ref
    cindex.CursorKind.MEMBER_REF: "chromaticaDeclRefExprCall",  # ex: designated initializer
    cindex.CursorKind.LABEL_REF: "chromaticaLableRef",
    cindex.CursorKind.OVERLOADED_DECL_REF: "chromaticaOverloadDeclRef",
    cindex.CursorKind.VARIABLE_REF: "chromaticaVariableRef",
# Errors
    cindex.CursorKind.INVALID_FILE: None,
    cindex.CursorKind.NO_DECL_FOUND: None,
    cindex.CursorKind.NOT_IMPLEMENTED: None,
    cindex.CursorKind.INVALID_CODE: None,
# Expressions
    cindex.CursorKind.UNEXPOSED_EXPR: None,
    cindex.CursorKind.DECL_REF_EXPR: TYPE_GROUP,
    cindex.CursorKind.MEMBER_REF_EXPR:
    {
        cindex.TypeKind.UNEXPOSED: "chromaticaMemberRefExprCall",  # member function call
    },
    cindex.CursorKind.CALL_EXPR: "chromaticaCallExpr",
    cindex.CursorKind.OBJC_MESSAGE_EXPR: "chromaticaObjCMessageExpr",
    cindex.CursorKind.BLOCK_EXPR: "chromaticaBlockExpr",

    # literals moved
    cindex.CursorKind.PAREN_EXPR: None,
    cindex.CursorKind.UNARY_OPERATOR: None,
    cindex.CursorKind.ARRAY_SUBSCRIPT_EXPR: None,
    cindex.CursorKind.BINARY_OPERATOR: None,
    cindex.CursorKind.COMPOUND_ASSIGNMENT_OPERATOR: None,
    cindex.CursorKind.CONDITIONAL_OPERATOR: None,
    cindex.CursorKind.CSTYLE_CAST_EXPR: None,
    cindex.CursorKind.INIT_LIST_EXPR: None,
    cindex.CursorKind.ADDR_LABEL_EXPR: None,
    cindex.CursorKind.StmtExpr: None,
    cindex.CursorKind.GENERIC_SELECTION_EXPR: None,
    cindex.CursorKind.GNU_NULL_EXPR: None,
    cindex.CursorKind.CXX_STATIC_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_DYNAMIC_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_REINTERPRET_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_CONST_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_FUNCTIONAL_CAST_EXPR: "chromaticaCast",
    cindex.CursorKind.CXX_TYPEID_EXPR: None,
    cindex.CursorKind.CXX_BOOL_LITERAL_EXPR: "chromaticaBoolean",
    cindex.CursorKind.CXX_NULL_PTR_LITERAL_EXPR: "chromaticaConstant",
    cindex.CursorKind.CXX_THIS_EXPR: "chromaticaStatement",

    cindex.CursorKind.CXX_THROW_EXPR: "chromaticaStatement",
    cindex.CursorKind.CXX_NEW_EXPR: "chromaticaStatement",
    cindex.CursorKind.CXX_DELETE_EXPR: "chromaticaStatement",
    cindex.CursorKind.CXX_UNARY_EXPR: "chromaticaStatement",
    cindex.CursorKind.OBJC_ENCODE_EXPR: None,
    cindex.CursorKind.OBJC_SELECTOR_EXPR: None,
    cindex.CursorKind.OBJC_PROTOCOL_EXPR: None,
    cindex.CursorKind.OBJC_BRIDGE_CAST_EXPR: None,
    cindex.CursorKind.PACK_EXPANSION_EXPR: None,
    cindex.CursorKind.SIZE_OF_PACK_EXPR: None,
    cindex.CursorKind.LAMBDA_EXPR: None,
    cindex.CursorKind.OBJ_BOOL_LITERAL_EXPR: None,
    cindex.CursorKind.OBJ_SELF_EXPR: None,
    cindex.CursorKind.OMP_ARRAY_SECTION_EXPR: None,

    cindex.CursorKind.UNEXPOSED_STMT: None,
    cindex.CursorKind.LABEL_STMT: "chromaticaStatement",
    cindex.CursorKind.COMPOUND_STMT: None,
    cindex.CursorKind.CASE_STMT: "chromaticaSwitch",
    cindex.CursorKind.DEFAULT_STMT: "chromaticaSwitch",
    cindex.CursorKind.IF_STMT: "chromaticaIf",
    cindex.CursorKind.SWITCH_STMT: "chromaticaSwitch",
    cindex.CursorKind.WHILE_STMT: "chromaticaLoop",
    cindex.CursorKind.DO_STMT: "chromaticaLoop",
    cindex.CursorKind.FOR_STMT: "chromaticaLoop",
    cindex.CursorKind.GOTO_STMT: "chromaticaStatement",
    cindex.CursorKind.INDIRECT_GOTO_STMT: "chromaticaStatement",
    cindex.CursorKind.CONTINUE_STMT: "chromaticaStatement",
    cindex.CursorKind.BREAK_STMT: "chromaticaStatement",
    cindex.CursorKind.RETURN_STMT: "chromaticaStatement",
    cindex.CursorKind.ASM_STMT: "chromaticaStatement",
    cindex.CursorKind.OBJC_AT_TRY_STMT: None,
    cindex.CursorKind.OBJC_AT_CATCH_STMT: None,
    cindex.CursorKind.OBJC_AT_FINALLY_STMT: None,
    cindex.CursorKind.OBJC_AT_THROW_STMT: None,
    cindex.CursorKind.OBJC_AT_SYNCHRONIZED_STMT: None,
    cindex.CursorKind.OBJC_AUTORELEASE_POOL_STMT: None,
    cindex.CursorKind.OBJC_FOR_COLLECTION_STMT: None,
    cindex.CursorKind.CXX_CATCH_STMT: "chromaticaExceptionStatement",
    cindex.CursorKind.CXX_TRY_STMT: "chromaticaExceptionStatement",
    cindex.CursorKind.CXX_FOR_RANGE_STMT: "chromaticaLoop",
    cindex.CursorKind.SEH_TRY_STMT: "chromaticaMSStatement",
    cindex.CursorKind.SEH_EXCEPT_STMT: "chromaticaMSStatement",
    cindex.CursorKind.SEH_FINALLY_STMT: "chromaticaMSStatement",
    cindex.CursorKind.MS_ASM_STMT: "chromaticaMSStatement",
    cindex.CursorKind.NULL_STMT: None,
    cindex.CursorKind.DECL_STMT: None,

    cindex.CursorKind.UNEXPOSED_ATTR: None,
    cindex.CursorKind.IB_ACTION_ATTR: None,
    cindex.CursorKind.IB_OUTLET_ATTR: None,
    cindex.CursorKind.IB_OUTLET_COLLECTION_ATTR: None,
    cindex.CursorKind.CXX_FINAL_ATTR: None,
    cindex.CursorKind.CXX_OVERRIDE_ATTR: None,
    cindex.CursorKind.ANNOTATE_ATTR: None,
    cindex.CursorKind.ASM_LABEL_ATTR: None,
    cindex.CursorKind.PACKED_ATTR: None,
    cindex.CursorKind.PURE_ATTR: None,
    cindex.CursorKind.CONST_ATTR: None,
    cindex.CursorKind.NODUPLICATE_ATTR: None,
    cindex.CursorKind.CUDACONSTANT_ATTR: None,
    cindex.CursorKind.CUDADEVICE_ATTR: None,
    cindex.CursorKind.CUDAGLOBAL_ATTR: None,
    cindex.CursorKind.CUDAHOST_ATTR: None,
    cindex.CursorKind.CUDASHARED_ATTR: None,
    cindex.CursorKind.VISIBILITY_ATTR: None,
    cindex.CursorKind.DLLEXPORT_ATTR: None,
    cindex.CursorKind.DLLIMPORT_ATTR: None,

    cindex.CursorKind.PREPROCESSING_DIRECTIVE: None,
    cindex.CursorKind.MACRO_DEFINITION: "chromaticaMacroDefinition",
    cindex.CursorKind.MACRO_INSTANTIATION: "chromaticaMacroInstantiation",
    cindex.CursorKind.INCLUSION_DIRECTIVE: "chromaticaInclusionDirective",
}

def _get_default_syn(cursor_kind):
    if cursor_kind.is_preprocessing():
        return "chromaticaPrepro"
    elif cursor_kind.is_declaration():
        return "chromaticaDecl"
    elif cursor_kind.is_reference():
        return "chromaticaRef"
    else:
        return "chromaticaDEFSYN"

def _get_keyword_decl_syn(cursor_kind):
    if cursor_kind == cindex.CursorKind.TYPE_ALIAS_DECL:
        return "chromaticaTypeAliasStatement"
    else:
        return "chromaticaType"

def _get_keyword_syn(cursor_kind):
    """Handles cursor type of keyword tokens. Providing syntax group for most
    keywords"""
    if cursor_kind.is_statement():
        return SYNTAX_GROUP.get(cursor_kind)
    elif cursor_kind.is_declaration(): # hack for function return type and others
        return _get_keyword_decl_syn(cursor_kind)
    elif cursor_kind.is_attribute():
        return SYNTAX_GROUP.get(cursor_kind)
    elif cursor_kind.is_expression():
        return SYNTAX_GROUP.get(cursor_kind)
    else:
        return "chromaticaKeyword"

def _get_syntax_group(token, cursor):
    if token.kind.value == 1: # Keyword
        return _get_keyword_syn(cursor.kind)

    elif token.kind.value == 2: # Identifier
        group = _get_default_syn(cursor.kind)

        _group = SYNTAX_GROUP.get(cursor.kind)
        if _group:
            if cursor.kind == cindex.CursorKind.DECL_REF_EXPR:
                _group = _group.get(cursor.type.kind)
                if _group:
                    group = _group
            elif cursor.kind == cindex.CursorKind.MEMBER_REF_EXPR:
                _group = _group.get(cursor.type.kind)
                if _group:
                    group = _group
                else:
                    group = "chromaticaMemberRefExprVar"
            else:
                group = _group
        return group

    elif token.kind.value == 3: # Literal
        literal_type = LITERAL_GROUP.get(cursor.kind)
        if literal_type:
            return literal_type
        else:
            return "%s" % literal_type

    elif token.kind.value == 4: # Comment
        return "Comment"

    else: # Punctuation
        return None

def get_highlight(tu, filename, lbegin, lend):
    file = tu.get_file(filename)

    if not file:
        return None, None

    begin = cindex.SourceLocation.from_position(tu, file, line=lbegin, column=1)
    end   = cindex.SourceLocation.from_position(tu, file, line=lend+1, column=1)
    tokens = tu.get_tokens(extent=cindex.SourceRange.from_locations(begin, end))

    syntax = {}

    for token in tokens:
        cursor = token.cursor
        cursor._tu = tu

        n_moreline = token.spelling.count("\n")
        if token.spelling[-1] == "\n":
            n_moreline = n_moreline - 1
        pos = [token.location.line, token.location.column, len(token.spelling), n_moreline]
        group = _get_syntax_group(token, cursor)

        if group:
            if group not in syntax:
                syntax[group] = []

            syntax[group].append(pos)

    return syntax

def get_highlight2(tu, filename, lbegin, lend):
    fp = open("AST_out.log", "w")
    file = tu.get_file(filename)

    if not file:
        return None

    begin = cindex.SourceLocation.from_position(tu, file, line=lbegin, column=1)
    end   = cindex.SourceLocation.from_position(tu, file, line=lend+1, column=1)
    tokens = tu.get_tokens(extent=cindex.SourceRange.from_locations(begin, end))

    syntax = {}
    output = {}

    for token in tokens:
        cursor = token.cursor
        cursor._tu = tu

        symbol = token.spelling
        pos = [token.location.line, token.location.column, len(token.spelling)]
        group = _get_syntax_group(token, cursor)

        if token.kind.value != 0:
            fp.write(bcolors.OKGREEN + "%s " % (symbol))
            if group:
                fp.write(bcolors.OKBLUE + "%s " % (group))
            else:
                fp.write(bcolors.WARNING + "%s " % (group))
            fp.write(bcolors.ENDC + "%s " % (pos))
            fp.write(bcolors.BOLD + "%s " % (token.kind))
            fp.write(bcolors.UNDERLINE + "%s " % (cursor.kind))
            fp.write(bcolors.HEADER + "%s" % (cursor.type.kind))
            fp.write(bcolors.ENDC + "\n")

    fp.close()

