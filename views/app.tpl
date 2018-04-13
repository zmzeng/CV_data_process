<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ app_title }}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/3.0.3/normalize.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/milligram/1.3.0/milligram.min.css">
    <link rel="stylesheet" href="https://milligram.github.io/styles/main.css">

  </head>
  <body>
    <header class="header" id="home">
      <section class="container">
        <img src="{{ app_ico }}" height="300"/>
        <p></p>
        <h1 class="title">{{ app_title }}</h1>
        <form action="{{ upload_href }}" method="POST" enctype="multipart/form-data">
          <div class="row">
            <div class="column column-30" style="text-align: center; margin:0 auto;">
              <input type="file" name="file_upload" />
            </div>
          </div>
          %for i in app_form:
          <div class="row" >
            <div class="column column-40" style="text-align: center; margin:0 auto;">
              <input type="{{ i['type'] }}" name="{{ i['name'] }}" placeholder="{{ i['placeholder'] }}">
            </div>
          </div>
          %end
          <div class="row">
            <div class="column" style="text-align: center; margin:0 auto;">
              <input type="submit" value="upload" />
              %if respones_status != "":
                  <p ><em style="color:red">{{ respones_status }}</em><br>
              %end
              %if download_link != "":
                  <a href="{{ download_link }}">
              %end
              %for i in response_info:
                  <em>{{ i }}</em><br>
              %end
              %if download_link != "":
                  </a>
              %end
                  </p>

            </div>
          </div>          
        </form>
        <p class="description">{{ app_description }}<br><i><small>code by zmzeng</small></i></p>
      </section>
    </header>
  </body>
</html>


