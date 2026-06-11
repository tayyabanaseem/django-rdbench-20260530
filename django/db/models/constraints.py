from django.db.models.expressions import Col
from django.db.models.query_utils import Q
from django.db.models.sql.compiler import SQLCompiler
from django.db.models.sql.expressions import SimpleCol


class BaseConstraint:
    def __init__(self, name):
        self.name = name

    def constraint_sql(self, model, schema_editor):
        raise NotImplementedError('This method must be implemented by a subclass.')

    def create_sql(self, model, schema_editor):
        raise NotImplementedError('This method must be implemented by a subclass.')

    def remove_sql(self, model, schema_editor):
        raise NotImplementedError('This method must be implemented by a subclass.')

    def deconstruct(self):
        path = '%s.%s' % (self.__class__.__module__, self.__class__.__name__)
        path = path.replace('django.db.models.constraints', 'django.db.models')
        return (path, (), {'name': self.name})

    def clone(self):
        _, args, kwargs = self.deconstruct()
        return self.__class__(*args, **kwargs)


class CheckConstraint(BaseConstraint):
    def __init__(self, *, check, name):
        self.check = check
        super().__init__(name)

    def _get_check_sql(self, model, schema_editor):
        query = Query(model=model)
        where = query.build_where(self.check)
        compiler = query.get_compiler(connection=schema_editor.connection)
        sql, params = where.as_sql(compiler, schema_editor.connection)
        return sql % tuple(schema_editor.quote_value(p) for p in params)

    def constraint_sql(self, model, schema_editor):
        check = self._get_check_sql(model, schema_editor)
        return schema_editor._check_sql(self.name, check)

    def create_sql(self, model, schema_editor):
        check = self._get_check_sql(model, schema_editor)
        return schema_editor._create_check_sql(model, self.name, check)

    def remove_sql(self, model, schema_editor):
        return schema_editor._delete_check_sql(model, self.name)

    def __repr__(self):
        return "<%s: check='%s' name=%r>" % (self.__class__.__name__, self.check, self.name)

    def __eq__(self, other):
        return (
            isinstance(other, CheckConstraint) and
            self.name == other.name and
            self.check == other.check
        )

    def deconstruct(self):
        path, args, kwargs = super().deconstruct()
        kwargs['check'] = self.check
        return path, args, kwargs


class UniqueConstraint(BaseConstraint):
        return super().deconstruct()


class CheckConstraint(BaseConstraint):
    def __init__(self, *, check, name):
        self.check = check
        self.name = name

    def constraint_sql(self, model, schema_editor):
        """Generate SQL for the check constraint, ensuring no table-qualified column names."""
        query = Query(model)
        where = query.build_where(self.check)
        
        # Convert Col nodes to SimpleCol to avoid table-qualified names in check constraints.
        # This prevents failures on SQLite and Oracle when tables are renamed during migrations.
        where = self._convert_cols_to_simplecol(where)
        
        compiler = SQLCompiler(query, schema_editor.connection, 'default')
        sql, params = compiler.compile(where)
        return 'CHECK (%s)' % sql, params
    
    def _convert_cols_to_simplecol(self, node):
        """
        Recursively convert Col nodes to SimpleCol in the constraint expression tree.
        
        This prevents fully qualified column names (e.g., "table"."column") in check
        constraints, which fail on SQLite and Oracle when the table is renamed during
        schema alterations. Only unqualified column names should appear in check constraints.
        
        Args:
            node: The expression node to convert (typically a Q object or Col expression).
        
        Returns:
            The converted node with all Col references replaced by SimpleCol.
        """
        if isinstance(node, Col):
            # Convert Col with table qualification to SimpleCol without qualification
            return SimpleCol(node.alias, node.output_field)
        
        if isinstance(node, Q):
            # Recursively process Q object children
            new_children = []
            for child in node.children:
                if isinstance(child, Q):
                    new_children.append(self._convert_cols_to_simplecol(child))
                else:
                    new_children.append(child)
            node.children = new_children
        
        return node
        return sql % tuple(schema_editor.quote_value(p) for p in params)

    def constraint_sql(self, model, schema_editor):
        fields = [model._meta.get_field(field_name).column for field_name in self.fields]
        condition = self._get_condition_sql(model, schema_editor)
        return schema_editor._unique_sql(model, fields, self.name, condition=condition)

    def create_sql(self, model, schema_editor):
        fields = [model._meta.get_field(field_name).column for field_name in self.fields]
        condition = self._get_condition_sql(model, schema_editor)
        return schema_editor._create_unique_sql(model, fields, self.name, condition=condition)

    def remove_sql(self, model, schema_editor):
        condition = self._get_condition_sql(model, schema_editor)
        return schema_editor._delete_unique_sql(model, self.name, condition=condition)

    def __repr__(self):
        return '<%s: fields=%r name=%r%s>' % (
            self.__class__.__name__, self.fields, self.name,
            '' if self.condition is None else ' condition=%s' % self.condition,
        )

    def __eq__(self, other):
        return (
            isinstance(other, UniqueConstraint) and
            self.name == other.name and
            self.fields == other.fields and
            self.condition == other.condition
        )

    def deconstruct(self):
        path, args, kwargs = super().deconstruct()
        kwargs['fields'] = self.fields
        if self.condition:
            kwargs['condition'] = self.condition
        return path, args, kwargs
