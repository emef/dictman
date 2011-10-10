var page = {};

function empty_w_obj() {
   return { 
       spelling: "",
       meanings: [{
           text: "",
           example: ""
       }],
       pos: "n",
       level: 1,
       derivatives: [],
       antonyms: [],
       synonyms: []
   };
}

function word_form(type, fn_complete, initial) {
    var d = $("#word_detail > .word_content");
    var initial = initial && initial.spelling ? initial : empty_w_obj();
    var main = $("<div />");
    var deriv = $("<div class='derivatives'/>");
    var deriv_btn = $("<button>add derivative</button>");
    var syn = $("<div />");
    var ant = $("<div />");
    var save_btn = $("<button>save word</button>");
    var errors_ul = $("<ul class='error_list'>");
    var d_num = 1;
    var fn_make_array = function(str) {
        var arr = str.replace(/\s+/g, '').split(',');
        return (arr[0] == "") ? [] : arr;
    }
    var fn_verify = function(w_obj) {
        var errors = [];
        var fn_verify_property = function(obj, property, i) {
            if (/^\s*$/.test(obj[property])) {
                if (i != null) 
                    errors.push(property + " required for derivative " + (i+1));
                else
                    errors.push(property + " required")
            }
        }
        var properties = ["spelling", "meaning", "example"];
        for (var i=0; i<properties.length; i++) {
            fn_verify_property(w_obj, properties[i]);
            for (var j=0; j<w_obj.derivatives.length; j++) {
                fn_verify_property(w_obj.derivatives[j], properties[i], j);
            }
        }
        return errors;
    }
    var fn_save = function() {
        var w_obj = {};
        w_obj.spelling = main.find("input[name=spelling]").val();
        w_obj.pos = main.find("select[name=pos]").val();
        w_obj.level = main.find("select[name=level]").val();
        w_obj.meanings = [{
            text: main.find("input[name=meaning]").val(),
            example: main.find("input[name=example]").val()
        }];
        w_obj.synonyms = fn_make_array(syn.find("input[name=synonyms]").val());
        w_obj.antonyms = fn_make_array(ant.find("input[name=antonyms]").val());

        w_obj.derivatives = []; 
        deriv.find("> div").map(function (i, der) {
            var d = $(der);
            w_obj.derivatives.push(
                { spelling: d.find("input[name=spelling]").val(),
                  pos: d.find("select").val(),
                  meanings: [{
                      text: d.find("input[name=meaning]").val(),
                      example: d.find("input[name=example]").val()
                  }]
                });
        });

        var errors = fn_verify(w_obj);
        if (errors.length == 0) {
            //d.children().remove();
            //D_word_detail.removeClass().addClass("loading");
            fn_complete(w_obj);
        } else {
            errors_ul.children().remove();
            for (var i=0; i<errors.length; i++) {
                errors_ul.append($("<li>" + errors[i] + "</li>"));
            }
        }
        
    }
    var fn_dropdown = function(options, name, val) {
        var result = $("<div>" + name + "</div>"),
            select = $("<select name=" + name + " />");
        for(var i=0; i<options.length; i++) {
            var key = options[i][0];
            var text = options[i][1];
            var opt = $("<option value='" + key + "' " +
                        (val == key ? "selected='selected'" : "") +
                        ">" + text + "</option>");
            select.append(opt);
        }
        result.append(select);
        return result;
    }
    var fn_pos = function(val) {
        return fn_dropdown([["n", "noun"],
                            ["v", "verb"],
                            ["P", "pronoun"],
                            ["adj", "adjective"],
                            ["adv", "adverb"]],
                           "pos",
                           val);
    }
    var fn_level = function(val) {
        return fn_dropdown([[1,1], [2,2], [3,3], [4,4], [5,5]],
                           "level",
                           val);
        }
    var fn_div_input = function(name, value) {
        return $("<div>" + name + ": " + 
                 "<input type='text' name='" + name + "' value='" + value + "' /></div>");
    }

    var fn_add_deriv = function(d_obj) {
        var d_obj = d_obj && d_obj.spelling ? d_obj : empty_w_obj();
        var sub = $("<div />");
        sub.append($("<h4>derivative " + d_num + "</h4>"));
        sub.append(fn_pos(d_obj.pos));
        sub.append(fn_div_input("spelling", d_obj.spelling));
        sub.append(fn_div_input("meaning", d_obj.meanings[0].text));
        sub.append(fn_div_input("example", d_obj.meanings[0].example));
        
        deriv.append(sub);
        d_num++;
    }

    /* clear  */
    d.children().remove();
    
    /* handlers */
    deriv_btn.click(fn_add_deriv);
    save_btn.click(fn_save);

    /* add derivatives if editing */
    for (var i=0; i<initial.derivatives.length; i++) {
        fn_add_deriv(initial.derivatives[i]);
    }
    
    /* patch together objects */
    var title = (type == "add") ? "Add new word" : "edit word: " + initial.spelling;
    main.append($("<h2>" + title + "</h2>"));
    main.append(errors_ul);
    main.append(fn_pos(initial.pos));
    main.append(fn_level(initial.level));
    main.append(fn_div_input("spelling", initial.spelling));
    main.append(fn_div_input("meaning", initial.meanings[0].text));
    main.append(fn_div_input("example", initial.meanings[0].example));
    d.append(main);

    d.append($("<h3>Derivatives</h4>"));
    d.append(deriv);
    d.append(deriv_btn);
    
    syn.append($("<h3>Synonyms</h4>"));
    syn.append($("<div>list: <input type='text' name='synonyms' /></div>"));
    syn.find("input").val(initial.synonyms.join(", "));
    d.append(syn);

    ant.append($("<h3>Antonyms</h4>"));
    ant.append($("<div>list: <input type='text' name='antonyms' /></div>"));
    ant.find("input").val(initial.antonyms.join(", "));
    d.append(ant);

    d.append(save_btn);

    return d;
}

(function(exports) {

    /* url constants */
    var GET_WORD_IDS = "/api/get_word_ids",
        GET_WORD = function(id) { return "/api/get_word/" + id },
        ADD_WORD = "/api/add_word",
        EDIT_WORD = "/api/edit_word",
        DEL_WORD = "/api/delete_word";
    
    
    /* POS map */
    var POS_MAP = {
        n: "noun",
        v: "verb",
        P: "Pronoun",
        adj: "adjective",
        adv: "adverb"
    };
    var POS = function(abrv) {
        return POS_MAP[abrv];
    }

    /* DOM references */
    var D_word_list,
        D_word_detail,
        D_word_content,
        D_searchbox,
        D_new_word_btn,
        D_add_word;
    
    /* globals */
    var words; /* holds all known words (for searching) */

//////////////////////////////////////////////////////////////////////////////////////////////
    /* add single word to word_list */
    exports.create_word = function(w_obj) {
        /* to lower case */
        w_obj.spelling = w_obj.spelling.toLowerCase();
        /* build word link DOM object */
        var d = $("<div />");
        var s = $("<span class='word-link'>" + w_obj.spelling + "</span>");
        d.append(s);
        /* add to word list */
        return {w_obj: w_obj, ref: d};
    }

    /* clear words_list */
    exports.clear_words = function() {
        D_word_list.children().remove();
    }

    /* given {w_obj, ref} object, add word to word_list */
    exports.add_word = function(obj) {
        obj.ref.find("span").click(function() { exports.word_detail(obj.w_obj.id) });
        D_word_list.append(obj.ref);
    }

//////////////////////////////////////////////////////////////////////////////////////////////
    /* filter word list (from search) */
    exports.filter = function(starts_with) {
        var re = new RegExp("^" + starts_with, "i"), 
            count = 0;
        exports.clear_words();
        for (var i=0, j=words.length; i<j; i++) {
            if (re.test(words[i].w_obj.spelling)) {
                exports.add_word(words[i]);
                count++;
            }
        }
        if (count == 0) {
            D_word_list.append($("<div>0 words match</div>"));
        }
    }

/////////////////////////////////////////////////////////////////////////////////////////////
    exports.get_id = function(spelling) {
        for (var i=0; i<words.length; i++) {
            if (spelling == words[i].w_obj.spelling) {
                return  words[i].w_obj.id;
            }
        }
        return null;
    }

/////////////////////////////////////////////////////////////////////////////////////////////
    /* query word detail info */
    exports.word_detail = function(id) {
        D_word_detail.removeClass().addClass("loading");
        $.ajax({
            type: "get",
            url: GET_WORD(id),
            dataType: "json",
            success: function(w_obj) {
                if (w_obj) {
                    exports.populate_detail(w_obj);
                    D_word_detail.removeClass().addClass("content");
                }
            }
        });  
    }

    /* populate the word_detail area */
    exports.populate_detail = function(w_obj) {
        var d = $("<div />")
        var add_word = function(obj, tag) {
            var sub = $("<div />"),
                ol = $("<ol />");
            if (!tag) tag = "h3";
            sub.append($("<" + tag + ">" + obj.spelling + "</" + tag + ">"));
            sub.append($("<div>" + POS(obj.pos) + "</div>"));
            
            for(var i=0, j=obj.meanings.length; i<j; i++) {
                ol.append($("<li>" + obj.meanings[i].text + "</li>" +
                            "<span><i>" + obj.meanings[i].example + "</i></span>"));
            }
            sub.append(ol);
            d.append(sub);
        }
        
        /* Clear old content */
        D_word_content.children().remove();

        /* add edit/delete button */
        if (is_admin) {
            var id = exports.get_id(w_obj.spelling);
            var edit_btn = $("<button>edit " + w_obj.spelling + "</button>");
            edit_btn.click(function() { exports.edit_word(w_obj, id) });
            D_word_content.append(edit_btn);

            var delete_btn = $("<button>delete " + w_obj.spelling + "</button>");
            delete_btn.click(function() { exports.delete_word(w_obj, id) });
            D_word_content.append(delete_btn);
        }
        
        add_word(w_obj, "h2");
        for(var i=0,j=w_obj.derivatives.length; i<j; i++) {
            add_word(w_obj.derivatives[i]);
        }

        d.append($("<h3>SYNONYMS</h3>"));
        d.append($("<span>" + w_obj.synonyms.join(", ") + "</span>"));

        d.append($("<h3>ANTONYMS</h3>"));
        d.append($("<span>" + w_obj.antonyms.join(", ") + "</span>"));

        D_word_content.append(d);
    }

////////////////////////////////////////////////////////////////////////////////////////////
    exports.start_add_word = function() {
        D_word_detail.removeClass().addClass("content");
        var fn_add = function (w_obj) {
            D_word_detail.removeClass().addClass("loading");
            $.ajax({
                type: "post",
                url: ADD_WORD,
                data: {w_obj: JSON.stringify(w_obj)},
                dataType: "json",
                success: function(obj) { 
                    D_word_detail.removeClass();
                    if (obj) {
                        obj = exports.create_word(obj);
                        words.push(obj);
                        exports.refresh_word_list();
                        exports.word_detail(obj.w_obj.id);
                    }
                }
            });
        }
        word_form("add", fn_add);
    }

/////////////////////////////////////////////////////////////////////////////////////////////
    exports.refresh_word_list = function() {
        D_word_list.children().remove();
        /* sort on w_obj.spelling key */
        words = words.sort(function(w1, w2) {
            return (w1.w_obj.spelling > w2.w_obj.spelling) ? 1 : -1;
        });
        /* now add to w_list */
        for(var i=0,j=words.length; i<j; i++) {
            exports.add_word(words[i]);
        }
    }

/////////////////////////////////////////////////////////////////////////////////////////////
    exports.edit_word = function(old_w_obj, id) {
        D_word_detail.removeClass().addClass("content");
        var fn_edit = function(w_obj) {
            w_obj.id = id;
            D_word_detail.removeClass().addClass("loading");
            $.ajax({
                type: "post",
                url: EDIT_WORD,
                data: {w_obj: JSON.stringify(w_obj)},
                dataType: "json",
                success: function(obj) { 
                    D_word_detail.removeClass();
                    if (obj) {
                        if (w_obj.spelling != old_w_obj.spelling) {
                            /*  HERE find old, move to end, pop, add new  */
                            for (var i=0; i<words.length; i++) {
                                if (words[i].w_obj.spelling == old_w_obj.spelling) {
                                    words[i] = exports.create_word(obj);
                                    break;
                                }
                            }
                            exports.refresh_word_list();
                        }
                        exports.word_detail(obj.id);
                    }
                }
            });
        }
        word_form("edit", fn_edit, old_w_obj);
    }

//////////////////////////////////////////////////////////////////////////////////////////////
    exports.delete_word = function(w_obj, id) {
        if (confirm("this will permanently remove " + w_obj.spelling + ", are you sure?")) {
            D_word_detail.removeClass().addClass("loading");
            $.ajax({
                type: "post",
                url: DEL_WORD,
                data: {id: id},
                dataType: "json",
                success: function(obj) {
                    D_word_detail.removeClass();
                    if (obj) {
                        for(var i=0; i<words.length; i++) {
                            if (words[i].w_obj.id == id) {
                                words[i] = words[words.length-1];
                                words.pop();
                                break;
                            }
                        }
                        exports.refresh_word_list();
                        
                    }
                }
            });
        }
    }
    
    exports.init = function() {
        /* initialize DOM references */
        D_word_list = $("#word_list");
        D_word_detail = $("#word_detail");
        D_word_content = $("#word_detail > .word_content");
        D_searchbox = $("#search_box");
        D_new_word_btn = $("#new_word");
        D_add_word = $("#word_add");

        /* add onchange listener to search box */
        D_searchbox.keyup(function() {
            exports.filter(D_searchbox.val());
        });

        /* on click for add word */
        D_new_word_btn.click(exports.start_add_word);
        
        /* get word list */
        $.ajax({
            type: "get",
            url: GET_WORD_IDS,
            dataType: "json",
            success: function(w_list) {
                if (w_list) {
                    words = [];
                    /* build words array */
                    for(var i=0,j=w_list.length; i<j; i++) {
                        var obj = exports.create_word(w_list[i]);
                        words.push(obj);
                    }
                    /* refresh (for first time) the word list */
                    exports.refresh_word_list();

                }
            }
        });
        
    }
    
})(page);

$(document).ready(page.init);