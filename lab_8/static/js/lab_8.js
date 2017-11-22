// FB initiation function
  window.fbAsyncInit = () => {
    FB.init({
      appId      : '145464169512675',
      cookie     : true,
      xfbml      : true,
      version    : 'v2.11'
    });

    // implementasilah sebuah fungsi yang melakukan cek status login (getLoginStatus)
    // dan jalankanlah fungsi render di bawah, dengan parameter true jika
    // status login terkoneksi (connected)

    FB.getLoginStatus(function(response){
        if(response.status == 'connected'){
          render(true);
        }else if(response.status == 'not_authorized'){
          facebookLogin();
        }else{
          facebookLogin();  
        }
    })

  };

  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "https://connect.facebook.net/en_US/sdk.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));

  const render = loginFlag => {
    if (loginFlag) {
      $('nav').html(
        '<nav class="navbar navbar-toggleable-md navbar-inverse" style="background-color:#3B5999;">'+
          '<button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">'+
            '<span class="navbar-toggler-icon"></span>'+
          '</button>'+
          '<a class="navbar-brand" href="#">Pesbuk</a>'+
          '<div class="collapse navbar-collapse" id="navbarNavDropdown">'+
            '<ul class="navbar-nav">'+
              '<li class="nav-item active">'+
                '<a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>'+
              '</li>'+
            '</ul>'+
            '<ul class="navbar-nav mr-auto">'+
              '<li class="nav-item">'+
                '<a class="nav-link" id="logout" onclick="facebookLogout()"> Logout <span class="sr-only">(current)</span></a>'+
              '</li>'+
            '</ul>'+
          '</div>'+
        '</nav>'
      )
      getUserData(user => {
        $('div#lab8').html(
          '<div class="profile">' +
            '<img class="cover" src="' + user.cover.source + '" alt="cover" />' +
            '<div class="data">' +
              '<table class="table ">'+
                '<thead>'+
                  '<tr>'+
                    '<td><img class="picture" src="'   + user.picture.data.url + '" alt="profpic" /></td>'+
                    '<th colspan="2"><h1>' + user.name + '</h1></th>' +
                  '</tr>'+
                '</thead>'+
                '<tbody>'+
                  '<tr>'+
                    '<td><h2> About Me </h2></td>'+ 
                    '<td><h2>' + user.about + '</h2></td>'+ 
                  '</tr>'+
                  '<tr>'+
                    '<td><h3> Birthday </h3></td>' +
                    '<td><h3>' + user.birthday + '</h3></td>' +
                  '</tr>'+
                  '<tr>'+
                    '<td><h3> Email </h3></td>' +
                    '<td><h3>' + user.email + '</h3></td>' +
                  '</tr>'+
                  '<tr>'+
                  '<td><h3> Gender </h3></td>' +
                  '<td><h3>' + user.gender + '</h3></td>' +
                '</tr>'+
                '</tbody>'+
              '</table>'+
            '</div>' +
          '</div>' +
          '<input type="text" class="form-control form-control-lg post" id="postInput" placeholder="Whats on your mind,'+ user.first_name +'?">'+
          '<button class="btn btn-primary postStatus" onclick="postStatus()">Post to Facebook</button>'+
          '<div class="feeds">'+
            '<h1>News Feed</h1>'+
          '</div>'+
          '<div class="d-flex flex-xl-column">'
        );

        getUserFeed(feed => {
          feed.data.map(value => {
            if (value.message && value.story) {
              $('div#lab8').append(
                '<div class="p-2">' +
                    '<table class="table">'+
                      '<tr>'+
                          '<p>' + value.message + '</p>' +
                          '<p>' + value.story + '</p>' +
                          '<button class="btn btn-danger delete" onclick="deleteStatus(\''+ value.id + '\') ">Delete</button>'+
                        '</tr>'+
                    '</table>'+
                 '</div>'
              );
            } else if (value.message) {
              $('div#lab8').append(
                '<div class="p-2">' +
                    '<table class="table">'+
                      '<tr>'+
                          '<p>' + value.message + '</p>' +
                          '<button class="btn btn-danger delete" onclick="deleteStatus(\''+ value.id + '\') ">Delete</button>'+
                        '</tr>'+
                    '</table>'+
                '</div>'
              );
            } else if (value.story) {
              $('div#lab8').append(
                '<div class="p-2">' +
                  '<p>' + value.story + '</p>' +
                  '<button class="btn btn-danger delete" onclick="deleteStatus(\''+ value.id + '\')">Delete</button>'+
                '</div>'
              );
            }
          });
        });
      });
    } else {
      $('div#lab8').html('');
    }
  };

  const facebookLogin = () => {
    FB.login(function(response) {
        if (response.authResponse) {
         console.log('Welcome!  Fetching your information.... ');
         render(false);
         render(true);
        } else {
         console.log('User cancelled login or did not fully authorize.');
        }
    },
      {scope : 'public_profile,email,user_about_me,user_birthday,user_posts,publish_actions'},
      {auth_type : 'reauthenticate'} 
    );
  };

  $('#login-button').click(facebookLogin);

  const facebookLogout = () => {
    FB.logout(function(response) {
          document.location.reload();
      });
  };
  
  const getUserData = (fun) => {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
          FB.api(
                '/me',
                {fields :'cover,picture,name,about,birthday,email,gender,first_name'},
                'GET',
                function(response){
                    console.log(response);
                    fun(response); 
                });
            }
         });
    };

  const getUserFeed = (fun) => {
    FB.getLoginStatus(function(response){
        if(response.status === 'connected'){
            FB.api(
                "/me/feed",
                function (response) {
                    if (response && !response.error) {
                        console.log(response);
                        fun(response);
                    }
                });
            }
        });
    };

  const postFeed = (message) => {
    FB.api(
        "/me/feed",
        "POST",
        {
            "message": message
        },
        function (response) {
          if (response && !response.error) {
              console.log('POST ID: ' + response.id);
              render(false);
              render(true);
          }else{
              alert('Error occured');
          }
        }
    );
  };

  const postStatus = () => {
    const message = $('#postInput').val();
    postFeed(message);
  };

  const deleteStatus = (id) => {
    var postId = id;
    FB.api(postId, 'delete', function(response) {
      if (!response || response.error) {
        alert('Error occured');
      } else {
        alert('Post was deleted');
        render(false);
        render(true);
      }
    });
  }
