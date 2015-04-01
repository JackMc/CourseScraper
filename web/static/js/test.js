$(function() {
  // Register all the things we want to run when a new page is loaded
  function load_page(thing) {
    obj = $(thing);
    id = obj.attr('id');
    $('.active').removeClass('active');
    obj.addClass('active');

    // Here goes whatever you want to do when you click a button.
    $("#content").load(id);
  }

  $('.nav li a').on('click', function() {load_page(this.parentNode)});

  // It already has the # for a selector!
  // Note that 'home' is a special case where 'hash' is ''
  load_page(location.hash === '' ? '#home' : location.hash);
});
