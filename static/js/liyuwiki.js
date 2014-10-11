/**
 * Created by Liyuwiki.com on 2014-8.
 */

window.onload=function(){
    var uplist = document.getElementsByClassName('up');
    var downlist = document.getElementsByClassName('down');
    var kw_list = document.getElementsByClassName('recent_search');
    var to_hide = document.getElementsByClassName('part_2');

    for(var i=0;i<to_hide.length;i++){
        to_hide[i].setAttribute('style', 'display:none;');
    }

    for(var i=0;i<kw_list.length;i++){
        var kw_href = kw_list[i].getAttribute('href');
        var kw_href = kw_href.substring(0, kw_href.length - 1);
        var modified_kw_href = kw_href.replace('add_search_term/', 'search/?q=');
        kw_list[i].setAttribute('href', modified_kw_href);
    }


    for(var i=0;i<uplist.length;i++){
        uplist[i].onclick = function(){
            var orient_up_href = this.getAttribute('href');
            var modified_up_href = orient_up_href.replace('.html?vote=add', '/action=add_vote');
            location.href = modified_up_href;
            return false;
        };
        downlist[i].onclick = function(){
            var orient_down_href = this.getAttribute('href');
            var modified_down_href = orient_down_href.replace('.html?vote=sub', '/action=sub_vote');
            location.href = modified_down_href;
            return false;
        };
    }


};