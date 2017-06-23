"""
Schemas to translate from database models to dictionaries.
"""

from apistar import schema


class Bibliography(schema.Object):
    properties = {
        "eid": schema.String(max_length=40),
        "created": schema.String(max_length=50),
        "modified": schema.String(max_length=50),
        "description": schema.String(max_length=float('inf')),
    }


class Document(schema.Object):
    properties = {
        'eid': schema.String(max_length=40),
        'created': schema.String(max_length=50),
        'modified': schema.String(max_length=50),
        'bibliography_eid': schema.String(max_length=40),
        'title': schema.String(max_length=512),
        'description': schema.String(max_length=float('inf')),
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


class RankingDescriptor(schema.Object):
    """
    Describes the options to create a term document matrix.
    """
    properties = {
        'matrix': schema.String(max_length=40),
        'covariance': schema.Number(minimun=0, maximum=1, default=0.8),
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


class MatrixFields(schema.Array):
    """
    An array of valid fields to pass to the create matrix constructor.
    """
    items = schema.Enum(enum=['title', 'description', 'keywords'])
    unique_items = True


class MatrixDescriptor(schema.Object):
    """
    Describes the options to create a term document matrix.
    """
    properties = {
        'bibliography': schema.String(max_length=40),
        'regularise': schema.Boolean(default=True),
        'fields': MatrixFields
    }
