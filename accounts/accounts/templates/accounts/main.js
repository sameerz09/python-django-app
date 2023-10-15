    
$(document).ready(function () {
// Fetch the account IDs from your Django view using AJAX
$.ajax({
 url: '/api/get-account-ids/',  // URL for the get_account_ids view
 type: 'GET',
 success: function (data) {
     // Clear existing options
     $('#selected_account_id').empty();

     // Add an empty default option
     $('#selected_account_id').append('<option value="">-- Select Account ID --</option>');

     // Add each account ID as an option in the select field
     $.each(data.account_ids, function (index, account_id) {
         $('#selected_account_id').append('<option value="' + account_id.toString() + '">' + account_id.toString() + '</option>');
     });
 },
 error: function (error) {
     console.error('Error:', error);
 }
});

$('#getBalanceSumButton').click(function () {
// Retrieve start_date, end_date, and selected_account_id values from the input fields
var start_date = $('#start_date').val();
var end_date = $('#end_date').val();
var selected_account_id = $('#selected_account_id').val();

// Check if "end_date" is required
if (end_date === '') {
 // Display the "End Date is required" message in red
 $('#response').html('<span style="color: red;">End date is required.</span>');

 // Clear the total_balance value
 $('#total_balance').empty();
 return; // Exit the function, preventing further processing
}

// Make an AJAX request to initiate GetBalanceSumView with dynamic dates and selected_account_id
$.ajax({
 url: '/api/get-balance-sum/',  // URL for the GetBalanceSumView
 type: 'GET',
 data: {
     start_date: start_date,
     end_date: end_date,
     selected_account_id: selected_account_id  // Include selected_account_id in the request
 },
 success: function (data) {
     // Clear existing content
     $('#response').empty();

     if (data.response.length > 0) {
         // Create a Bootstrap table to display the response data
         var tableHtml = '<table class="table">';
         tableHtml += '<thead><tr><th>Account ID</th><th>Account Name</th><th>Balance</th><th>Root ID</th><th>Movement Date</th></tr></thead><tbody>';
         $.each(data.response, function (index, item) {
             tableHtml += '<tr>';
             tableHtml += '<td>' + item.account_id + '</td>';
             tableHtml += '<td>' + item.account_name + '</td>';
             tableHtml += '<td>' + item.balance + '</td>';
             tableHtml += '<td>' + item.root_id + '</td>';
             tableHtml += '<td>' + item.date + '</td>';
             tableHtml += '</tr>';
         });
         tableHtml += '</tbody></table>';
         $('#response').html(tableHtml);

         // Display the total_balance value
         $('#total_balance').text('Total Balance: ' + data.total_balance);
     } else {
         // Handle the case when the response is empty
         $('#response').text('No data available.');

         // Clear the total_balance value
         $('#total_balance').empty();
     }
 },
 error: function (error) {
     // Handle any errors (if needed)
     console.error('Error:', error);
 }
});
});
});
     document.getElementById('resetFormButton').addEventListener('click', function () {
     document.getElementById('start_date').value = ''; // Reset start_date input
     document.getElementById('end_date').value = '';   // Reset end_date input
     document.getElementById('selected_account_id').value = ''; // Reset selected_account_id input
 });

