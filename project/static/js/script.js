$(document).ready(function(){
  $('.navbar-toggler').click(function(){
    $('body').append('<div class="modal-backdrop fade show"></div>').addClass('modal-open nav-open');
  });

  $('.search-open').click(function(){
      $('body').append('<div class="modal-backdrop fade show"></div>').addClass('modal-open top-header-open');
  });

  $(document).on('click','.modal-backdrop, .search-close',function(){
      $('body').removeClass('modal-open nav-open top-header-open filter-open');
      $('.modal-backdrop').remove();
  });

  $('.search-input-clear').click(function(){
    $('.search-input').val('').focus();
  });
});