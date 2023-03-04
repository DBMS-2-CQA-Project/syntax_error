const tag = document.getElementById("autosearch");
var hidden_tag = document.getElementById("autosearch_hidden");


const tagify = new Tagify(tag, {
  whitelist: [],
  enforceWhitelist: true,
  maxTags: 5,
  autocomplete: {
    enabled: true,
    minLength: 1,
    maxItems: 10
  },
  callbacks: {
    add: function (e) {

      var tags = tagify.value.map(tag => tag.value).join(' ');
      hidden_tag.value = tags;


    },
    remove: function (e) {
      console.log("Tag removed :", e.detail.data.value);
      var tags = tagify.value.map(tag => tag.value).join(' ');
      hidden_tag.value = tags;

    }


  }


});

var data = {% autoescape on %}
{ { avail_users | safe } }
{% endautoescape %};

tagify.settings.maxTags = 1;
tagify.settings.whitelist = data;

$('#searchBy').on('change', function () {
  var selectedOption = $(this).val();

  var data = [];

  // Update the tagify whitelist based on the selected option
  if (selectedOption == 'username') {
    data = {% autoescape on %}
  { { avail_users | safe } }
  {% endautoescape %};
  tagify.settings.maxTags = 1;

}
   else if (selectedOption == 'tags') {
  data = {{ avail_tags | safe }
};
  }
tagify.settings.whitelist = data;
tagify.settings.maxTags = 5;
  
});