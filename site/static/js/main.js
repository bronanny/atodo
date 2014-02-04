
var weird_data_format = "X ZZ";
var picker;

var ViewModel = {
  username: ko.observable(''),
  todos: ko.observableArray(),
  loading: ko.observable(false),

  recv_todo: function (todo) {
    var td = this.todo_from_ID(todo.ID);
    if (!_.isUndefined(td)) {
      this.todos.splice(this.todos.indexOf(td), 1, todo);
    } else {
      this.todos.push(todo);
    }
  },

  nid: ko.observable(NaN),
  next_id: function () {
    if (!this.todos().length) { return 0; }
    if (_.isNaN(this.nid())) {
      return 1 + _.max(this.todos(), function(td){ return td.ID; }).ID;
    }
    var nid = this.nid();
    this.nid(NaN);
    return nid;
  },

  cancel_edit: function(){
    this.nid(NaN);
  },

  sort_direction: 1,
  sortdd_direction: 1,

  sort_by: function (d, field) {
    this.todos.sort(function(left, right){
      return left[field] == right[field] ? 0 : (left[field] < right[field] ? -d : d);
    });
  },

  sort_by_priority: function () {
    this.sort_direction = -this.sort_direction;
    this.sort_by(this.sort_direction, 'priority');
  },

  sort_by_due_date: function () {
    this.sortdd_direction = -this.sortdd_direction;
    this.sort_by(this.sortdd_direction, 'due_date');
  },

  todo_from_ID: function (ID) {
    return _.findWhere(this.todos(), {ID: ID});
  },

  delete_todo: function (todo) {
    $.ajax({
      type: 'DELETE',
      url: '/api/todo/' + todo.ID,
      success: function(){ ViewModel.todos.remove(todo); },
      error: function(xhr, type){ alert(type); }
    });
  },

  edit_todo: function (todo) {
    ViewModel.nid(todo.ID);
    $("#body").val(todo.body);
    $("#priority").val(todo.priority);
    picker.setMoment(moment(todo.due_date, weird_data_format));
  },

  send_todo_basic: function (ID, body, priority, date, completed) {
    $.post(
      '/todo/' + ID,
      {ID: ID, body: body, priority: priority,
       due_date: date, completed: completed},
      function(data){ ViewModel.recv_todo(data.todo); },
      "json"
    );
  },

  complete_todo: function (todo) {
    ViewModel.send_todo_basic(
      todo.ID,
      todo.body,
      todo.priority,
      todo.due_date,
      true
    );
  },

  submit_todo: function () {
    var o = _.indexBy($('form').serializeArray(), 'name');
    this.send_todo_basic(
      this.next_id(),
      o.body.value,
      o.priority.value,
      o.date.value,
      false // automatically set un-completed.
    );
  }

};

$(document).ready(function(){

  ko.applyBindings(ViewModel);

  picker = new Pikaday({
    field: $('#datepicker')[0],
    onSelect: function() {
      $('#date').val(this.getMoment().format(weird_data_format));
    },
    minDate: new Date(),
    maxDate: new Date('2024-12-31'),
    yearRange: [2014, 2024],
    format: "dddd, MMMM Do YYYY"
    });

  $(document).on('ajaxBeforeSend', function(){ ViewModel.loading(true); })
             .on('ajaxComplete', function(){ ViewModel.loading(false); });

  $.get('/todos', function(data){ ViewModel.todos(data.todos); });

});

