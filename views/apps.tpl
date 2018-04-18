% rebase('base.tpl')

    <div class="ui vertical container segment">
      <div class="ui center aligned container">
        <img src={{ app_ico }} height="350">
        <h1 class="title">{{ app_title }}</h1>
        <p class="description">{{ app_description }}</p>
        <form action="{{ upload_href }}" method="POST" enctype="multipart/form-data">
          <div class="ui container">
            <div class="field">
                <div class="ui action file input">
                    <input type="file" id="file" name="file_upload" multiple="multiple">
                    <label for="file" class="ui icon button"><i class="attach icon"></i></label>
                </div>
            </div>
          </div>
          %for i in app_form:
          <div class="ui container">
              <input type="{{ i['type'] }}" name="{{ i['name'] }}" placeholder="{{ i['placeholder'] }}">
          </div>
          %end
          <div class="ui vertical segment">
            <div class="field">
                <label for="upload" id="upload_button" class="ui primary button">Upload</label>
                <input type="submit" id="upload" value="upload" style="display:none" onclick="changeStatus()">
            </div>
            <div class="ui vertical segment">
              %if respones_status != "":
                  <p><em style="color:red">{{ respones_status }}</em><br>
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
      </div>
    </div>

    <script type="text/javascript">
    function changeStatus()
    {
        document.getElementById("upload_button").className="ui primary loading button";
    }
    </script>
