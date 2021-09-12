ace.define("ace/mode/shnootalk_highlight_rules",["require","exports","module","ace/lib/oop","ace/mode/text_highlight_rules"], function(require, exports, module) {
    "use strict";
    
    var oop = require("../lib/oop");
    var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;
    
    var ShnooTalkHighlightRules = function() {
    
        this.$rules = {
            start: [{
                token: "comment.line.number-sign.shnootalk",
                regex: /#[^\n\r]*/,
                comment: "Single line comment"
            }, {
                token: "keyword.control.shnootalk",
                regex: /\b(?:use|as|from|begin|end|if|elif|else|while|do|for|loop|break|continue|return|void)\b/,
                comment: "Keywords"
            }, {
                token: "keyword.operator.shnootalk",
                regex: /\b(?:and|or|not)\b/,
                comment: "Conditional operators"
            }, {
                token: "string.quoted.double.shnootalk",
                regex: /"/,
                push: [{
                    token: "string.quoted.double.shnootalk",
                    regex: /"/,
                    next: "pop"
                }, {
                    token: "constant.character.escape.shnootalk",
                    regex: /\\./
                }, {
                    defaultToken: "string.quoted.double.shnootalk"
                }],
                comment: "String literal"
            }, {
                token: "constant.numeric.integer.hexadecimal.shnootalk",
                regex: /\b0x[a-fA-f0-9]+\b/,
                comment: "Hex literal"
            }, {
                token: "constant.numeric.shnootalk",
                regex: /\b0b[0-1]+\b/,
                comment: "Bin literal"
            }, {
                token: "constant.numeric.shnootalk",
                regex: /\b[0-9]*\.[0-9]+\b/,
                comment: "Float literal"
            }, {
                token: "string.quoted.single.shnootalk",
                regex: /'\\?.'/,
                comment: "Character literal"
            }, {
                token: "constant.numeric.shnootalk",
                regex: /\b[0-9]+\b/,
                comment: "Integer literal"
            }, {
                token: "constant.language.boolean.shnootalk",
                regex: /\b(?:true|false)\b/,
                comment: "Boolean literal"
            }, {
                token: "storage.type.shnootalk",
                regex: /\b(?:var|const|mut)\b/,
                comment: "Declaration type"
            }, {
                token: "storage.type.shnootalk",
                regex: /\b(?:fn|extfn)\b/,
                comment: "'fn' keyword"
            }, {
                token: ["support.function.shnootalk", "text"],
                regex: /\b([a-zA-Z_][a-zA-Z0-9_]*)\b(\()/,
                comment: "Function name"
            }, {
                token: [
                    "storage.type.shnootalk",
                    "text",
                    "entity.name.type.shnootalk"
                ],
                regex: /\b(struct|class)(\s+)([a-zA-Z_][a-zA-Z0-9_]*)\b/,
                push: [{
                    token: "text",
                    regex: /[\{\(;]/,
                    next: "pop"
                }],
                comment: "User defined type definition"
            }, {
                token: "storage.type.shnootalk",
                regex: /\b(?:enum|def)\b/,
                comment: "Used defined enum and def"
            }, {
                token: [
                    "entity.name.scope-resolution.shnootalk",
                    "text"
                ],
                regex: /([a-zA-Z_][a-zA-Z0-9_]*)(::)/,
                comment: "Module scope"
            }, {
                token: "text",
                regex: /(?:->|\:)/,
                next: "type",
                comment: "Type"
            }, {
                token: ["entity.name.type.shnootalk", "text", "text"],
                regex: /\b([a-zA-Z_][a-zA-Z0-9_]*)(\s*)(\[\]`|\*`|`)/,
                comment: "Cast type"
            }, {
                token: "variable.name.shnootalk",
                regex: /\b[a-zA-Z_][a-zA-Z0-9_]*\b/,
                comment: "Symbol or identifier"
            }],
            type: [{
                token: [
                    "entity.name.scope-resolution.shnootalk",
                    "text"
                ],
                regex: /([a-zA-Z_][a-zA-Z0-9_]*)(::)/,
                comment: "Module scope"
            }, {
                token: "entity.name.type.shnootalk",
                regex: /\b[a-zA-Z_][a-zA-Z0-9_]*\b/,
                comment: "Symbol or identifier",
                next: "start"
            }]
        }
        
        this.normalizeRules();
    };
    
    ShnooTalkHighlightRules.metaData = {
        "$schema": "https://raw.githubusercontent.com/martinring/tmlanguage/master/tmlanguage.json",
        name: "ShnooTalk",
        scopeName: "source.shnootalk"
    }
    
    
    oop.inherits(ShnooTalkHighlightRules, TextHighlightRules);
    
    exports.ShnooTalkHighlightRules = ShnooTalkHighlightRules;
    });

ace.define("ace/mode/folding/cstyle",["require","exports","module","ace/lib/oop","ace/range","ace/mode/folding/fold_mode"], function(require, exports, module) {
"use strict";

var oop = require("../../lib/oop");
var Range = require("../../range").Range;
var BaseFoldMode = require("./fold_mode").FoldMode;

var FoldMode = exports.FoldMode = function(commentRegex) {
    if (commentRegex) {
        this.foldingStartMarker = new RegExp(
            this.foldingStartMarker.source.replace(/\|[^|]*?$/, "|" + commentRegex.start)
        );
        this.foldingStopMarker = new RegExp(
            this.foldingStopMarker.source.replace(/\|[^|]*?$/, "|" + commentRegex.end)
        );
    }
};
oop.inherits(FoldMode, BaseFoldMode);

(function() {
    
    this.foldingStartMarker = /([\{\[\(])[^\}\]\)]*$|^\s*(\/\*)/;
    this.foldingStopMarker = /^[^\[\{\(]*([\}\]\)])|^[\s\*]*(\*\/)/;
    this.singleLineBlockCommentRe= /^\s*(\/\*).*\*\/\s*$/;
    this.tripleStarBlockCommentRe = /^\s*(\/\*\*\*).*\*\/\s*$/;
    this.startRegionRe = /^\s*(\/\*|\/\/)#?region\b/;
    this._getFoldWidgetBase = this.getFoldWidget;
    this.getFoldWidget = function(session, foldStyle, row) {
        var line = session.getLine(row);
    
        if (this.singleLineBlockCommentRe.test(line)) {
            if (!this.startRegionRe.test(line) && !this.tripleStarBlockCommentRe.test(line))
                return "";
        }
    
        var fw = this._getFoldWidgetBase(session, foldStyle, row);
    
        if (!fw && this.startRegionRe.test(line))
            return "start"; // lineCommentRegionStart
    
        return fw;
    };

    this.getFoldWidgetRange = function(session, foldStyle, row, forceMultiline) {
        var line = session.getLine(row);
        
        if (this.startRegionRe.test(line))
            return this.getCommentRegionBlock(session, line, row);
        
        var match = line.match(this.foldingStartMarker);
        if (match) {
            var i = match.index;

            if (match[1])
                return this.openingBracketBlock(session, match[1], row, i);
                
            var range = session.getCommentFoldRange(row, i + match[0].length, 1);
            
            if (range && !range.isMultiLine()) {
                if (forceMultiline) {
                    range = this.getSectionRange(session, row);
                } else if (foldStyle != "all")
                    range = null;
            }
            
            return range;
        }

        if (foldStyle === "markbegin")
            return;

        var match = line.match(this.foldingStopMarker);
        if (match) {
            var i = match.index + match[0].length;

            if (match[1])
                return this.closingBracketBlock(session, match[1], row, i);

            return session.getCommentFoldRange(row, i, -1);
        }
    };
    
    this.getSectionRange = function(session, row) {
        var line = session.getLine(row);
        var startIndent = line.search(/\S/);
        var startRow = row;
        var startColumn = line.length;
        row = row + 1;
        var endRow = row;
        var maxRow = session.getLength();
        while (++row < maxRow) {
            line = session.getLine(row);
            var indent = line.search(/\S/);
            if (indent === -1)
                continue;
            if  (startIndent > indent)
                break;
            var subRange = this.getFoldWidgetRange(session, "all", row);
            
            if (subRange) {
                if (subRange.start.row <= startRow) {
                    break;
                } else if (subRange.isMultiLine()) {
                    row = subRange.end.row;
                } else if (startIndent == indent) {
                    break;
                }
            }
            endRow = row;
        }
        
        return new Range(startRow, startColumn, endRow, session.getLine(endRow).length);
    };
    this.getCommentRegionBlock = function(session, line, row) {
        var startColumn = line.search(/\s*$/);
        var maxRow = session.getLength();
        var startRow = row;
        
        var re = /^\s*(?:\/\*|\/\/|--)#?(end)?region\b/;
        var depth = 1;
        while (++row < maxRow) {
            line = session.getLine(row);
            var m = re.exec(line);
            if (!m) continue;
            if (m[1]) depth--;
            else depth++;

            if (!depth) break;
        }

        var endRow = row;
        if (endRow > startRow) {
            return new Range(startRow, startColumn, endRow, line.length);
        }
    };

}).call(FoldMode.prototype);

});

ace.define("ace/mode/shnootalk",["require","exports","module","ace/lib/oop","ace/mode/text","ace/mode/shnootalk_highlight_rules","ace/mode/folding/cstyle"], function(require, exports, module) {
  "use strict";
  
  var oop = require("../lib/oop");
  var TextMode = require("./text").Mode;
  var ShnooTalkHighlightRules = require("./shnootalk_highlight_rules").ShnooTalkHighlightRules;
  var FoldMode = require("./folding/cstyle").FoldMode;
  
  var Mode = function() {
      this.HighlightRules = ShnooTalkHighlightRules;
      this.foldingRules = new FoldMode();
  };
  oop.inherits(Mode, TextMode);
  
  (function() {
      this.lineCommentStart = "#";
      this.$id = "ace/mode/shnootalk"
  }).call(Mode.prototype);
  
  exports.Mode = Mode;
  });                (function() {
                    ace.require(["ace/mode/shnootalk"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            