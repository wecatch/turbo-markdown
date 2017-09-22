template_html = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Document</title>
  # <link rel="stylesheet" type="text/css" href="/static/css/semantic.min.css">
  <script type="text/javascript" src="/static/js/jquery-3.2.1.min.js" ></script>
      <style type="text/css" media="screen">
        html, body, div, span,
        h1, h2, h3, h4, h5, h6, p,
        a , em, img, strong, i,
        ol, ul, li, form, label {
          margin: 0;
          padding: 0;
          border: 0;
          font-size: 14px;
          vertical-align: baseline;
          line-height: 16px;
        }

        ol, ul {
          list-style: none;
        }

        body {
          background-color: #fff;
          min-height: 100%;
        }

        a {
          outline: none;
          text-decoration: none;
        }

        img {
          width: auto;
          height: auto;
        }

        .nav-list {
            padding-left: 15px;
            padding-right: 15px;
            margin-bottom: 0px;
        }

        .nav-list li {
            line-height: 20px;
        }

        .nav-list > li > a {
            margin-left: -15px;
            margin-right: -15px;
            text-shadow: rgba(255, 255, 255, 0.5) 0px 1px 0px;
            padding: 3px 15px;
            display: block;
            color: #08c;
            line-height: 20px;
        }

        .nav-list > li > a:hover {
            background: #eee;
        }

        .has-sub ul {
            /*display: none;*/
        }

        .main-wrapper {
            margin-left: 320px;
        }

        .doc-tree {
            position: fixed;
            width: 300px;
            top:0;
            left: 0;
            border-right: 1px solid #ccc;
            background-color: #f5f5f5;
            overflow-y: auto;
            height: 100%;
            min-height: 100%;

            h3 {
                margin: 0px;
                text-align: center;
            }
        }

        .doc-content {

        }
    </style>
</head>
<body>
  <div class="doc-tree js-doc-tree" >
    <h3>tree </h3>
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