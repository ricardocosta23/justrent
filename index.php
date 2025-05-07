<?php
// Initialize variables
$errorMessage = "";
$successMessage = "";
$id = "";
$address = "";

// Process form submission
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Validate inputs
    if (empty($_POST["id"]) || empty($_POST["address"])) {
        $errorMessage = "Both ID and address fields are required.";
    } else {
        $id = filter_input(INPUT_POST, 'id', FILTER_VALIDATE_INT);
        $address = trim($_POST["address"]);
        
        if ($id === false) {
            $errorMessage = "ID must be a valid integer.";
        } else {
            // Database connection parameters
            $servername = "localhost";
            $username = "justrentmalta";
            $password = "KmCji@5BxmiWK";
            $dbname = "jrm_db";
            
            try {
                // Create connection using PDO
                $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
                
                // Set the PDO error mode to exception
                $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                
                // Prepare and execute the update statement
                $stmt = $conn->prepare("UPDATE properties_old SET address = :address WHERE id = :id");
                $stmt->bindParam(':address', $address);
                $stmt->bindParam(':id', $id, PDO::PARAM_INT);
                $stmt->execute();
                
                // Check if any rows were affected
                if ($stmt->rowCount() > 0) {
                    $successMessage = "Address updated successfully!";
                    // Clear the form fields after successful update
                    $id = "";
                    $address = "";
                } else {
                    $errorMessage = "No property found with the provided ID.";
                }
                
                // Close the connection
                $conn = null;
            } catch(PDOException $e) {
                $errorMessage = "Database error: " . $e->getMessage();
            }
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Property Address</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h2 class="text-center">Update Property Address</h2>
                    </div>
                    <div class="card-body">
                        <?php if (!empty($errorMessage)): ?>
                            <div class="alert alert-danger">
                                <?php echo htmlspecialchars($errorMessage); ?>
                            </div>
                        <?php endif; ?>
                        
                        <?php if (!empty($successMessage)): ?>
                            <div class="alert alert-success">
                                <?php echo htmlspecialchars($successMessage); ?>
                            </div>
                        <?php endif; ?>
                        
                        <form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>">
                            <div class="mb-3">
                                <label for="id" class="form-label">Property ID:</label>
                                <input type="number" class="form-control" id="id" name="id" value="<?php echo htmlspecialchars($id); ?>" required>
                            </div>
                            
                            <div class="mb-3">
                                <label for="address" class="form-label">New Address:</label>
                                <textarea class="form-control" id="address" name="address" rows="3" required><?php echo htmlspecialchars($address); ?></textarea>
                            </div>
                            
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary">Update Address</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Simple form validation
        document.querySelector('form').addEventListener('submit', function(e) {
            const idField = document.getElementById('id');
            const addressField = document.getElementById('address');
            
            if (idField.value.trim() === '' || addressField.value.trim() === '') {
                e.preventDefault();
                alert('Both ID and address fields are required.');
            }
        });
    </script>
</body>
</html>
