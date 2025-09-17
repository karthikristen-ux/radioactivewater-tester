# ---- TAB 5 ----
with tabs[4]:
    st.subheader("📁 Dataset Viewer & Editor")
    
    try:
        df = pd.read_csv("water_data.csv")
        
        # Ensure "Elements Found" column exists
        if "Elements Found" not in df.columns:
            df["Elements Found"] = df.apply(lambda row: detect_elements(row["pH"], row["TDS"], row["Hardness"], row["Nitrate"]), axis=1)
        
        # Multiselect for columns to display
        cols = st.multiselect("Select parameters to display", df.columns.tolist(), default=df.columns.tolist())
        st.dataframe(df[cols])
        
        # Select rows to delete based on Location
        remove_locations = st.multiselect("Select Locations to Remove", df["Location"].unique())
        if st.button("Remove Selected Locations"):
            df = df[~df["Location"].isin(remove_locations)]
            df.to_csv("water_data.csv", index=False)
            st.success("Selected locations removed successfully ✅")
            st.dataframe(df[cols])
        
        # Option to download updated dataset
        st.download_button("📥 Download Updated Dataset", data=df.to_csv(index=False), file_name="water_data.csv", mime="text/csv")
        
    except FileNotFoundError:
        st.info("No dataset found yet. Run an analysis first.")
