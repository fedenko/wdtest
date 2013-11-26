csrfSafeMethod = (method) ->

  # these HTTP methods do not require CSRF protection
  /^(GET|HEAD|OPTIONS|TRACE)$/.test method
sameOrigin = (url) ->

  # test that a given url is a same-origin URL
  # url could be relative or scheme relative or absolute
  host = document.location.host # host + port
  protocol = document.location.protocol
  sr_origin = "//" + host
  origin = protocol + sr_origin

  # Allow absolute or scheme relative URLs to same origin

  # or any other URL that isn't scheme relative or absolute i.e relative.
  (url is origin or url.slice(0, origin.length + 1) is origin + "/") or (url is sr_origin or url.slice(0, sr_origin.length + 1) is sr_origin + "/") or not (/^(\/\/|http:|https:).*/.test(url))
getCookie = (name) ->
  cookieValue = null
  if document.cookie and document.cookie isnt ""
    cookies = document.cookie.split(";")
    i = 0

    while i < cookies.length
      cookie = jQuery.trim(cookies[i])

      # Does this cookie string begin with the name we want?
      if cookie.substring(0, name.length + 1) is (name + "=")
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      i++
  cookieValue

class window.PopoverWidget
  constructor: (@el) ->
    @template = $("#context-menu-content").html()
    @imageId = $(@el).data("image-id")
    self = @
    $(@el).bind "click", ->
      e = $(this)
      e.unbind "click"
      $.ajax
        url: "/lists/get/"
        type: "post"
        dataType: "json"
        data:
          image_id: self.imageId

        success: (data) ->
          unless data.success
            alert data.error
          else
            self.updatePopover data
            self.showPopover()
        error: (xhr, err) ->
          alert "Error"

  render: (data) ->
    Mustache.render(@template, data)

  updatePopover: (data) ->
    self = @
    e  = $(@el)
    if e.data("popover")
      e.popover 'destroy'
    e.popover
      html: true
      content: @render
        imageId: @imageId
        lists: data.lists
    tip = e.data("popover").tip()
    tip.on "submit", ".add-list", ->
      $.ajax
        url: "/lists/add/"
        type: "post"
        dataType: "json"
        data: $(this).serialize()
        success: (data) ->
          unless data.success
            alert data.error
          else
            self.updatePopover data
            self.showPopover()
        error: (xhr, err) ->
          alert "Error"

      false
    return

  showPopover: ->
    $(@el).popover "show"

$ ->
  $.ajaxSetup beforeSend: (xhr, settings) ->
    if not csrfSafeMethod(settings.type) and sameOrigin(settings.url)

      # Send the token to same-origin, relative URLs only.
      # Send the token only if the method warrants CSRF protection
      # Using the CSRFToken value acquired earlier
      csrftoken = getCookie("csrftoken")
      xhr.setRequestHeader "X-CSRFToken", csrftoken


  $(".context-menu-btn").each ->
    pw = new PopoverWidget(@)
    $(@).data("popoverwidget", pw)
