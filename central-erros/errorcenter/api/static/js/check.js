$(function () {
  $('#logTable').DataTable({
      dom: 'Bfrtip',
      responsive: true,
      buttons: {
          buttons: [
              { extend: 'selectAll', className: 'bg-red waves-effect' },
              { extend: 'selectNone', className: 'bg-red waves-effect' },
              { extend: 'copy', className: 'bg-red waves-effect' },
              { extend: 'csv', className: 'bg-red waves-effect' },
              { extend: 'excel', className: 'bg-green waves-effect' },
              { extend: 'print', className: 'bg-red waves-effect' },
          ],
      },
      'columnDefs': [{
          'targets': 0,
          'orderable': false,
          'className': 'select-checkbox',
          'checkboxes': {
              'selectRow': true
          }
      }],
      'select': {
          'style': 'multi',
      },
      'order': [
          [1, 'asc']
      ]
  });
});