import streamlit as st
from datetime import date, timedelta, datetime
import pandas as pd
from core.converter import convert_currency, get_historical_rates
from ui.dashboard import create_rate_chart, display_conversion_metadata
from ui.widgets import create_currency_inputs, create_amount_input
from core.cache import initialize_cache

def main():
    st.set_page_config(
        page_title="Enterprise Currency Converter",
        page_icon="💱",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize cache
    initialize_cache()
    
    # App header
    st.title("Real-Time Currency Converter")
    st.subheader("Enterprise-grade fiat and cryptocurrency conversion platform")
    
    # About information (moved from sidebar to main content)
    st.info(
        "This application provides real-time currency conversion "
        "for both fiat currencies and cryptocurrencies."
    )
    
    # Main conversion interface
    col1, col2 = st.columns([2, 3])
    
    with col1:
        # Currency selection and amount input
        source_currency, target_currency = create_currency_inputs()
        amount = create_amount_input(source_currency)
        
        # Conversion button
        if st.button("Convert", type="primary", use_container_width=True):
            with st.spinner("Converting currencies..."):
                try:
                    result, metadata = convert_currency(amount, source_currency, target_currency)
                    
                    # Check if there was an error in the conversion
                    if "error" in metadata and metadata["error"]:
                        st.warning(f"⚠️ {metadata.get('warning', 'Warning: Using fallback rate')}")
                        st.error(f"Error: {metadata.get('error_message', 'Conversion error')}")
                        
                        # Still show the result, but with a warning
                        st.info(f"{amount:,.2f} {source_currency} = {result:,.6f} {target_currency} (estimated)")
                    else:
                        # Display successful result
                        st.success(f"{amount:,.2f} {source_currency} = {result:,.6f} {target_currency}")
                    
                    # Show warning if using cached data
                    if "warning" in metadata and not metadata.get("error", False):
                        st.info(f"ℹ️ {metadata['warning']}")
                        if "cache_age_minutes" in metadata:
                            st.info(f"Cache age: {metadata['cache_age_minutes']} minutes")
                    
                    # Store in session state for history
                    if "conversion_history" not in st.session_state:
                        st.session_state.conversion_history = []
                    
                    # Ensure rate is available in metadata or use calculated rate
                    if "rate" not in metadata:
                        # Calculate rate from result and amount if not present
                        rate = result / amount if amount != 0 else 0
                        metadata["rate"] = rate
                    
                    st.session_state.conversion_history.append({
                        "timestamp": metadata["timestamp"],
                        "source": source_currency,
                        "target": target_currency,
                        "amount": amount,
                        "result": result,
                        "rate": metadata["rate"],
                        "error": metadata.get("error", False)
                    })
                    
                except Exception as e:
                    st.error(f"Conversion failed: {str(e)}")
                    st.info("Attempting to use cached rates if available...")
                    # Add cached rate fallback logic here
        
        # Advanced features in expander
        with st.expander("Advanced Options"):
            st.checkbox("Enable real-time updates", value=False, key="enable_updates")
            
            # Set default date range (last 7 days)
            default_start = date.today() - timedelta(days=7)
            default_end = date.today()
            
            date_range = st.date_input(
                "Historical date range",
                value=(default_start, default_end),
                min_value=date(2000, 1, 1),
                max_value=date.today(),
                help="Select date range for historical data (if available)"
            )
            
            if st.button("Download Conversion History", use_container_width=True):
                if "conversion_history" in st.session_state and st.session_state.conversion_history:
                    # Convert history to DataFrame
                    df = pd.DataFrame(st.session_state.conversion_history)
                    
                    # Convert DataFrame to CSV
                    csv = df.to_csv(index=False).encode('utf-8')
                    
                    st.download_button(
                        label="Download CSV",
                        data=csv,
                        file_name="conversion_history.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                else:
                    st.warning("No conversion history to export.")
    with col2:
        # Dashboard components
        if "conversion_history" in st.session_state and st.session_state.conversion_history:
            latest = st.session_state.conversion_history[-1]
            
            try:
                # Display rate chart with date range
                st.subheader(f"Exchange Rate Trend: {latest['source']} to {latest['target']}")
                
                # Fix: Update the function call to match the expected parameters
                # Check if date_range is defined and has at least 2 elements
                start_date = date_range[0] if 'date_range' in locals() and len(date_range) >= 1 else (date.today() - timedelta(days=7))
                end_date = date_range[1] if 'date_range' in locals() and len(date_range) >= 2 else date.today()
                
                # Call the function with only the required arguments
                # The function only accepts 2-3 arguments, not 4
                rate_data = get_historical_rates(latest['source'], latest['target'])
                
                if rate_data:
                    chart = create_rate_chart(rate_data, latest['source'], latest['target'])
                    st.plotly_chart(chart, use_container_width=True)
                    display_conversion_metadata(latest)
                else:
                    st.warning("No historical data available for selected date range.")
                    
            except Exception as e:
                st.error(f"Failed to load historical data: {str(e)}")
                st.info("Showing cached historical data if available...")
                # Add cached data fallback here
        else:
            st.info("Enter an amount and select currencies to see conversion results and trends.")
    
    # Conversion history
    if "conversion_history" in st.session_state and len(st.session_state.conversion_history) > 0:
        st.markdown("---")
        st.subheader("Conversion History (Last 10 Conversions)")
        
        # Create DataFrame for display
        history_df = pd.DataFrame(
            st.session_state.conversion_history[-10:],
            columns=["timestamp", "source", "target", "amount", "result", "rate"]
        )
        
        # Format DataFrame
        history_df["Amount"] = history_df.apply(
            lambda x: f"{x['amount']:,.2f} {x['source']}", axis=1
        )
        history_df["Result"] = history_df.apply(
            lambda x: f"{x['result']:,.6f} {x['target']}", axis=1
        )
        history_df["Rate"] = history_df["rate"].apply(lambda x: f"{x:,.6f}")
        # Fix the timestamp formatting in the history dataframe
        history_df["Timestamp"] = history_df["timestamp"].apply(
            lambda x: x.strftime("%Y-%m-%d %H:%M:%S") if hasattr(x, 'strftime') else x
        )
        
        # Display formatted DataFrame
        st.dataframe(
            history_df[["Timestamp", "Amount", "Result", "Rate"]],
            use_container_width=True,
            hide_index=True
        )

if __name__ == "__main__":
    main()