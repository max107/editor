"""This indenter works according to    
    http://community.schemewiki.org/?scheme-style
    
TODO support (module
"""

from qutepart.indenter.base import IndenterBase


class IndenterScheme(IndenterBase):
    """Indenter for Scheme files
    """
    TRIGGER_CHARACTERS = ""

    def _findExpressionEnd(self, block):
        """Find end of the last expression
        """
        while block.isValid():
            column = self._lastColumn(block)
            if column > 0:
                return block, column
            block = block.previous()
        raise UserWarning()

    def _lastWord(self, text):
        """Move backward to the start of the word at the end of a string.
        Return the word
        """
        for index, char in enumerate(text[::-1]):
            if char.isspace() or \
               char in ('(', ')'):
                return text[len(text) - index :]
        else:
            return text
        
    def _findExpressionStart(self, block):
        """Find start of not finished expression
        Raise UserWarning, if not found
        """
        
        # raise expession on next level, if not found
        expEndBlock, expEndColumn = self._findExpressionEnd(block)
        
        text = expEndBlock.text()[:expEndColumn + 1]
        if text.endswith(')'):
            try:
                return self.findBracketBackward(expEndBlock, expEndColumn, '(')
            except ValueError:
                raise UserWarning()
        else:
            return expEndBlock, len(text) - len(self._lastWord(text))

    def computeIndent(self, block, char):
        """Compute indent for the block
        """
        try:
            foundBlock, foundColumn = self._findExpressionStart(block.previous())
        except UserWarning:
            return ''
        expression = foundBlock.text()[foundColumn:].rstrip()
        beforeExpression = foundBlock.text()[:foundColumn].strip()
        
        if beforeExpression.startswith('(module'):  # special case
            return ''
        elif beforeExpression.endswith('define'):  # special case
            return ' ' * (len(beforeExpression) - len('define') + 1)
        elif beforeExpression.endswith('let'):  # special case
            return ' ' * (len(beforeExpression) - len('let') + 1)
        else:
            return ' ' * foundColumn
