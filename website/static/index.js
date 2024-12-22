// Select the form and table body
const form = document.querySelector('form');
const tableBody = document.querySelector('tbody');

// Function to create a table row
function createTableRow() {
  const row = document.createElement('tr');

  // PART NO. / DESCRIPTION
  const partNoCell = document.createElement('td');
  partNoCell.innerHTML = '<input type="text" name="partNo[]" >';
  row.appendChild(partNoCell);

  // CATEGORY
  const categoryCell = document.createElement('td');
  categoryCell.innerHTML = '<input type="text" name="category[]" >';
  row.appendChild(categoryCell);

  // MAKE
  const makeCell = document.createElement('td');
  makeCell.innerHTML = '<input type="text" name="make[]" >';
  row.appendChild(makeCell);

  // QTY (Ordered Qty)
  const qtyCell = document.createElement('td');
  qtyCell.innerHTML = '<input type="number" name="qty[]" min="0" >';
  row.appendChild(qtyCell);

  // TDS APPROVAL
  const tdsCell = document.createElement('td');
  const tdsSelect = document.createElement('select');
  tdsSelect.name = "approvedNotapporoved[]";
  tdsSelect.required = true;
  tdsSelect.innerHTML = `
    <option value="approved">Approved</option>
    <option value="Notapproved">Not Approved</option>
  `;
  tdsCell.appendChild(tdsSelect);
  row.appendChild(tdsCell);

  // Billable/Non Billable
  const billableCell = document.createElement('td');
  const billableSelect = document.createElement('select');
  billableSelect.name = "billableNonBillable[]";
  billableSelect.required = false;
  billableSelect.innerHTML = `
    <option value="billable">Billable</option>
    <option value="nonBillable">Non Billable</option>
  `;
  billableCell.appendChild(billableSelect);
  row.appendChild(billableCell);

  // Ordered Qty
  const orderedQtyCell = document.createElement('td');
  orderedQtyCell.innerHTML = '<input type="number" name="orderedQty[]" min="0" >';
  row.appendChild(orderedQtyCell);

  // Order Status
  const orderStatusCell = document.createElement('td');
  const orderStatusSelect = document.createElement('select');
  orderStatusSelect.name = "orderStatus[]";
  orderStatusSelect.required = true;
  orderStatusSelect.innerHTML = `
    <option value="pending">Pending</option>
    <option value="confirmed">Confirmed</option>
    <option value="cancelled">Cancelled</option>
  `;
  orderStatusCell.appendChild(orderStatusSelect);
  row.appendChild(orderStatusCell);

  // PODATE
  const podateCell = document.createElement('td');
  podateCell.innerHTML = '<input type="date" name="podate[]" >';
  row.appendChild(podateCell);

  // DELIVERY PERIOD
  const deliveryPeriodCell = document.createElement('td');
  deliveryPeriodCell.innerHTML = '<input type="text" name="deliveryPeriod[]" >';
  row.appendChild(deliveryPeriodCell);

  // Dispatch status
  const disStatusCell = document.createElement('td');
  const disStatusSelect = document.createElement('select');
  disStatusSelect.name = "disStatus[]";
  disStatusSelect.required = true;
  disStatusSelect.innerHTML = `
    <option value="pending">Pending</option>
    <option value="confirmed">Confirmed</option>
    <option value="cancelled">Cancelled</option>
  `;
  disStatusCell.appendChild(disStatusSelect);
  row.appendChild(disStatusCell);

  // DELIVERY AT
  const deliveryAtCell = document.createElement('td');
  deliveryAtCell.innerHTML = '<input type="text" name="deliveryAt[]" >';
  row.appendChild(deliveryAtCell);

  // SUPPLIED QTY
  const suppliedQtyCell = document.createElement('td');
  suppliedQtyCell.innerHTML = '<input type="number" name="suppliedQty[]" min="0" >';
  row.appendChild(suppliedQtyCell);

  // DELIVERY STATUS
  const deliveryStatusCell = document.createElement('td');
  const deliveryStatusSelect = document.createElement('select');
  deliveryStatusSelect.name = "deliveryStatus[]";
  deliveryStatusSelect.required = true;
  deliveryStatusSelect.innerHTML = `
    <option value="pending">Pending</option>
    <option value="completed">Completed</option>
    <option value="delayed">Delayed</option>
  `;
  deliveryStatusCell.appendChild(deliveryStatusSelect);
  row.appendChild(deliveryStatusCell);

  // BACKLOG QTY
  const backlogQtyCell = document.createElement('td');
  backlogQtyCell.innerHTML = '<input type="text" name="backlogQty[]" >';
  row.appendChild(backlogQtyCell);

  // REMARKS
  const remarksCell = document.createElement('td');
  remarksCell.innerHTML = '<input type="text" name="remarks[]">';
  row.appendChild(remarksCell);

  // Append the row to the table body
  tableBody.appendChild(row);
}

// Event listener for form submission
form.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the form from submitting

  // Collect the form data
  const formData = new FormData(form);
  const formObject = Object.fromEntries(formData.entries());

  // Calculate totals
  const approvedTDS = formData.getAll('approvedNotapporoved[]').filter(status => status === 'approved').length;
  const notApprovedTDS = formData.getAll('approvedNotapporoved[]').filter(status => status === 'Notapproved').length;

  const pendingOrders = formData.getAll('orderStatus[]').filter(status => status === 'pending').length;
  const confirmedOrders = formData.getAll('orderStatus[]').filter(status => status === 'confirmed').length;
  const cancelledOrders = formData.getAll('orderStatus[]').filter(status => status === 'cancelled').length;

  const pendingDeliveries = formData.getAll('disStatus[]').filter(status => status === 'pending').length;
  const completedDeliveries = formData.getAll('disStatus[]').filter(status => status === 'confirmed').length;
  const delayedDeliveries = formData.getAll('disStatus[]').filter(status => status === 'cancelled').length;
  const all = formData.getAll('approvedNotapporoved[]').length;

  // Prepare URL parameters
  const params = new URLSearchParams();
  params.append('approvedTDS', approvedTDS);
  params.append('notApprovedTDS', notApprovedTDS);
  params.append('pendingOrders', pendingOrders);
  params.append('confirmedOrders', confirmedOrders);
  params.append('cancelledOrders', cancelledOrders);
  params.append('pendingDeliveries', pendingDeliveries);
  params.append('completedDeliveries', completedDeliveries);
  params.append('delayedDeliveries', delayedDeliveries);
  params.append('all', all);

  // Redirect with URL parameters
  window.location.href = `display.html?${params.toString()}`;
});

// Initial row creation (if needed)
createTableRow();

// Select the addRowBtn button by its ID
const addRowBtn = document.getElementById('addRowBtn');

// Add event listener for click event
addRowBtn.addEventListener('click', function(event) {
    event.preventDefault(); // Prevent button default behavior (e.g., form submission)
    
    createTableRow(); // Call function to create a new table row
});
