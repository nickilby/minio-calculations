import streamlit as st

def calculate_erasure_coding_usage(file_size, nodes, drives_per_node):
    """Calculate storage usage in erasure-coded MinIO setup"""
    total_drives = nodes * drives_per_node
    
    # MinIO follows EC: k+N where k = 3/4 of total drives and N = 1/4 (rounded)
    data_shards = int(0.75 * total_drives)  # k
    parity_shards = total_drives - data_shards  # N
    
    if data_shards == 0:
        return 0, 0, 0  # No storage
    
    # Storage Usage Calculation
    storage_multiplier = total_drives / data_shards
    storage_used = file_size * storage_multiplier
    
    return storage_used, data_shards, parity_shards

def main():
    st.title("📊 MinIO Storage Calculator")
    st.markdown("Calculate MinIO storage usage based on erasure coding and replication settings.")
    
    # User Inputs
    file_size = st.number_input("Enter File Size (MB)", min_value=0.1, value=1.0, step=0.1)
    nodes = st.number_input("Number of Nodes", min_value=1, value=4, step=1)
    drives_per_node = st.number_input("Drives per Node", min_value=1, value=4, step=1)
    
    replication_enabled = st.checkbox("Enable Replication?")
    replication_factor = st.slider("Replication Factor", 2, 5, 2) if replication_enabled else 1

    # Calculate Erasure Coding Storage
    storage_used, data_shards, parity_shards = calculate_erasure_coding_usage(file_size, nodes, drives_per_node)
    
    if storage_used > 0:
        st.subheader("💾 Storage Calculation")
        st.write(f"**Total Drives:** {nodes * drives_per_node}")
        st.write(f"**Erasure Coding Scheme:** {data_shards} data + {parity_shards} parity")
        st.write(f"**Storage Used (without replication):** {storage_used:.2f} MB")
        
        # Adjust for Replication
        if replication_enabled:
            replicated_storage = storage_used * replication_factor
            st.write(f"**Storage Used (with replication factor {replication_factor}):** {replicated_storage:.2f} MB")
        else:
            st.write("**Replication is disabled**")
    
    else:
        st.error("Invalid configuration. Increase number of nodes or drives.")

if __name__ == "__main__":
    main()
