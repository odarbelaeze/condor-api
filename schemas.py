"""
Schemas to translate from database models to dictionaries.
"""

from apistar import schema


class Bibliography(schema.Object):
    properties = {
        "eid": schema.String(max_length=40),
        "created": schema.String(max_length=50),
        "modified": schema.String(max_length=50),
        "description": schema.String(max_length=100),
    }


class Document(schema.Object):
    properties = {
        'eid': schema.String(max_length=40),
        'created': schema.String(max_length=50),
        'modified': schema.String(max_length=50),
        'bibliography_eid': schema.String(max_length=40),
        'title': schema.String(max_length=40),
        'description': schema.String(max_length=512),
        'keywords': schema.String(max_length=512),
        'language': schema.String(max_length=16)
    }


class Ranking(schema.Object):
    properties = {
        "eid": schema.String(max_length=40),
        'created': schema.String(max_length=50),
        'modified': schema.String(max_length=50),
        "term_document_matrix_eid": schema.String(max_length=40),
        "kind": schema.String(max_length=16),
        "build_options": schema.String(max_length=512),
    }


class Matrix(schema.Object):
    properties = {
        "eid": schema.String(max_length=40),
        'created': schema.String(max_length=50),
        'modified': schema.String(max_length=50),
        "bibliography_eid": schema.String(max_length=40),
        "bibliography_options": schema.String(max_length=512),
        "processing_options": schema.String(max_length=512),
    }


class MatrixDescriptor(schema.Object):
    """
    Describes the options to create a term document matrix.
    """
    properties = {
        'bibliography': schema.String(max_length=40),
        'regularise': schema.Boolean(default=True),
        # TODO: schema.Array(of_enum), not available in 0.1.17
        'fields': schema.String(max_length=100),
    }
