import pandas as pd

def partition_barcodes_by_sample_type(barcodes):
    # Define a dictionary to store partitioned barcodes by sample type names
    '''
    # Example usage
    barcodes = [
    "TCGA-02-0001-01C-01D-0182-01",
    "TCGA-02-0002-02C-01D-0182-01",
    "TCGA-02-0003-03C-01D-0182-01",
    "TCGA-02-0001-01C-01D-0182-02"
    ]
    
    partitioned_barcodes = partition_barcodes_by_sample_type(barcodes)
    
    # Print the result
    print(partitioned_barcodes)
    '''
    sample_type_names = {
        "01": "primary_solid_tumor",
        "02": "recurrent_solid_tumor",
        "03": "primary_blood_derived_cancer_peripheral_blood",
        "04": "recurrent_blood_derived_cancer_bone_marrow",
        "05": "additional_new_primary",
        "06": "metastatic",
        "07": "additional_metastatic",
        "08": "human_tumor_original_cells",
        "09": "primary_blood_derived_cancer_bone_marrow",
        "10": "blood_derived_normal",
        "11": "solid_tissue_normal",
        "12": "buccal_cell_normal",
        "13": "ebv_immortalized_normal",
        "14": "bone_marrow_normal",
        "15": "sample_type_15",
        "16": "sample_type_16",
        "20": "control_analyte",
        "40": "recurrent_blood_derived_cancer_peripheral_blood",
        "50": "cell_lines",
        "60": "primary_xenograft_tissue",
        "61": "cell_line_derived_xenograft_tissue",
        "99": "sample_type_99"
    }
    
    partitioned_barcodes = {}
    patient_samples = {}

    # Convert input to a pandas Series if it is not already
    if isinstance(barcodes, list):
        barcodes = pd.Series(barcodes)
    elif isinstance(barcodes, pd.DataFrame):
        barcodes = barcodes.squeeze()  # Converts DataFrame column/row to Series if needed

    # Extract sample type code from each barcode
    for barcode in barcodes:
        sample_type_code = barcode[13:15]
        patient_id = barcode[8:12]
        sample_type_name = sample_type_names.get(sample_type_code, "unknown_sample_type")

        if sample_type_name == "unknown_sample_type":
            print(f"Warning: Unknown sample type code: {sample_type_code}")
            continue
        
        # Initialize a list for the sample type name if it doesn't exist
        if sample_type_name not in partitioned_barcodes:
            partitioned_barcodes[sample_type_name] = []
        
        # Append the barcode to the corresponding sample type name list
        partitioned_barcodes[sample_type_name].append(barcode)

        # Track patient samples to detect duplicates
        if patient_id not in patient_samples:
            patient_samples[patient_id] = {}
        
        if sample_type_name not in patient_samples[patient_id]:
            patient_samples[patient_id][sample_type_name] = []

        patient_samples[patient_id][sample_type_name].append(barcode)
        
        # Warning for multiple samples of the same type from the same patient
        if len(patient_samples[patient_id][sample_type_name]) > 1:
            print(f"Warning: Multiple samples of the same type for patient {patient_id}: {sample_type_name}")

    return partitioned_barcodes

