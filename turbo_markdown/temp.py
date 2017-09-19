template_html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
  <link rel="stylesheet" type="text/css" href="/static/css/joydoc.css">
  <link rel="stylesheet" type="text/css" href="/static/css/joydoc-responsive.css">
  <script type="text/javascript" src="/static/js/jquery-2.0.3.js" ></script>
  <script type="text/javascript" src="/static/js/bootstrap.js" ></script>
  <link rel="stylesheet" type="text/css" href="/static/css/pygements/colorful.css">
</head>
<body>
  <div class="doc-tree js-doc-tree" >
    <h3>tree </h3>
    {% raw html_tree %}
  </div>
  <div class="container-fluid fluid-height main-wrapper" >
    <div class="row-fluid" >
      <div class="span12" >
        <div class="doc-content js-doc-content codehilite" >
          {% raw html %}
        </div>
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