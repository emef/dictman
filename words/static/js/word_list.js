var page = {};

(function(exports) {

    /* url constants */
    var GET_WORD_IDS = "/api/get_word_ids",
        GET_WORD = function(id) { return "/api/get_word/" + id };

    /* DOM references */
    var D_word_list,
        D_word_detail,
        D_word_content,
        D_searchbox;
    
    /* globals */
    var words; /* holds all known words (for searching) */
    
    /* add single word to word_list */
    exports.create_word = function(w_obj) {
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

    exports.filter = function(starts_with) {
        var re = new RegExp("^" + starts_with), 
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

    /* query word detail info */
    exports.word_detail = function(id) {
        D_word_detail.removeClass().addClass("loading");
        $.ajax({
            type: "post",
            url: GET_WORD(id),
            dataType: "json",
            success: function(w_obj) {
                if (w_obj) {
                    exports.populate_detail(w_obj);
                    D_word_detail.removeClass().addClass("detail");
                }
            }
        });  
    }

    /* populate the word_detail area */
    exports.populate_detail = function(w_obj) {
        var d = $("<div />");

        /* clear old content */
        D_word_content.children().remove();

        d.append($("<h3>" + w_obj.spelling + "</h3>"));

        D_word_content.append(d);
    }
        
    
    exports.init = function() {
        /* initialize DOM references */
        D_word_list = $("#word_list");
        D_word_detail = $("#word_detail");
        D_word_content = $("#word_detail > .word_content");
        D_searchbox = $("#word_search > input");

        /* add onchange listener to search box */
        D_searchbox.keyup(function() {
            exports.filter(D_searchbox.val());
        });
        
        /* get word list */
        $.ajax({
            type: "post",
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
                    /* sort on w_obj.spelling key */
                    words = words.sort(function(w1, w2) {
                        return (w1.w_obj.spelling > w2.w_obj.spelling) ? 1 : -1;
                    });
                    /* now add to w_list */
                    for(var i=0,j=words.length; i<j; i++) {
                        exports.add_word(words[i]);
                    }

                }
            }
        });
        
    }
    
})(page);

$(document).ready(page.init);