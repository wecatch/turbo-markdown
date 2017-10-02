import hashlib
import os.path


TEMPLATE_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>
  <link rel="stylesheet" href="/static/css/github.css?v=css_version">
  <script type="text/javascript" src="/static/js/jquery-3.2.1.min.js" ></script>
</head>
<body>
  <div class="doc-tree js-doc-tree" >
    {% raw html_tree %}
  </div>
  <div class="ui grid main-wrapper" >
    <div class="row" >
        <div class="doc-content js-doc-content codehilite" >
          {% raw html %}
        </div>
    </div>
  </div>

  <script type="text/javascript">
    var gDocCache = {};

    $("a.js-has-sub").on("click",function (e) {
      e.preventDefault();
      $(this).parent().find("ul:first").slideToggle();
    });

    $("div.js-doc-tree").on("click","a",function(e){
      e.preventDefault();
      var $this = $(this);
      if($this.hasClass("js-has-sub")) return;

      var path = $this.attr("href");
      var title = $this.html();
      document.title = title;
      pushHistoryState(path, title, path);
      fetchHtmlContent(path);
    });


    function pushHistoryState(state, title, url) {
      if (window.history.pushState) {
        history.pushState(state, title, url);
      } else {
        window.location.href = window.location.host + path;
      }
    }

    function fetchHtmlContent(path){
      if(!path)return;
      var key = path.replace(/\//gi,'_');
      var cacheData = gDocCache[key];
      var docContent = $("div.js-doc-content");
      if(cacheData){
        docContent.html(cacheData);
        return;
      }

      $.get(path).done(function(data){
        docContent.html(data);
        gDocCache[key] = data;
      }).fail(function(){
        docContent.html("something wrong, please try");
      });
    }

    onpopstate = function(e){
      fetchHtmlContent(e.state);
    }
  </script>
</body>
</html>
"""


css_v = hashlib.md5(
    open(os.path.join(
        os.path.dirname(__file__),
        'static/css/github.css'), 'r').read()).hexdigest()[0:6]

template_html = TEMPLATE_HTML.replace('css_version', css_v)
