import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import datetime

def create_rate_chart(rate_data: List[Dict[str, Any]], source: str, target: str) -> go.Figure:
    """
    Create an interactive line chart showing exchange rate trends.
    
    Args:
        rate_data: List of dictionaries with date and rate information
        source: Source currency code
        target: Target currency code
        
    Returns:
        Plotly figure object
    """
    dates = [entry["date"] for entry in rate_data]
    rates = [entry["rate"] for entry in rate_data]
    
    fig = go.Figure()
    
    # Add main line
    fig.add_trace(go.Scatter(
        x=dates,
        y=rates,
        mode='lines+markers',
        name=f'{source} to {target}',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8)
    ))
    
    # Calculate min and max for range
    min_rate = min(rates) * 0.95
    max_rate = max(rates) * 1.05
    
    # Configure layout
    fig.update_layout(
        title=f'{source} to {target} Exchange Rate - Last 7 Days',
        xaxis_title='Date',
        yaxis_title=f'Exchange Rate (1 {source} in {target})',
        hovermode='x unified',
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(204, 204, 204, 0.2)',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(204, 204, 204, 0.2)',
            range=[min_rate, max_rate]
        ),
        plot_bgcolor='rgba(255, 255, 255, 0.0)',
        paper_bgcolor='rgba(255, 255, 255, 0.0)',
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    # Add current rate line
    current_rate = rates[-1]
    fig.add_shape(
        type="line",
        x0=dates[0],
        y0=current_rate,
        x1=dates[-1],
        y1=current_rate,
        line=dict(
            color="red",
            width=1,
            dash="dash",
        )
    )
    
    # Add annotation for latest rate
    fig.add_annotation(
        x=dates[-1],
        y=current_rate,
        text=f"Current: {current_rate:.6f}",
        showarrow=True,
        arrowhead=1,
    )
    
    return fig

def display_conversion_metadata(conversion_data: Dict[str, Any]):
    """
    Display metadata about a conversion in a formatted panel.
    
    Args:
        conversion_data: Dictionary containing conversion metadata
    """
    st.subheader("Conversion Details")
    
    # Create a visually appealing container
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Exchange Rate",
                value=f"{conversion_data['rate']:.6f}",
                delta=None
            )
            
            # Format the timestamp
            timestamp = conversion_data.get("timestamp", "")
            if isinstance(timestamp, str):
                try:
                    # Parse ISO format timestamp if possible
                    dt = datetime.datetime.fromisoformat(timestamp)
                    formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    formatted_time = timestamp
            else:
                formatted_time = str(timestamp)
            
            st.info(f"📅 Last updated: {formatted_time}")
            
        with col2:
            # Create a metadata table
            metadata_items = []
            
            # Extract relevant metadata
            if "source_api" in conversion_data:
                metadata_items.append({"Key": "API Source", "Value": conversion_data["source_api"]})
            
            if "cached" in conversion_data and conversion_data["cached"]:
                cache_status = "Cached Data"
                if "cache_expired" in conversion_data and conversion_data["cache_expired"]:
                    cache_status += " (Expired)"
                metadata_items.append({"Key": "Status", "Value": cache_status})
                
                if "cache_age" in conversion_data:
                    age_seconds = conversion_data["cache_age"]
                    if age_seconds < 60:
                        age_text = f"{int(age_seconds)} seconds ago"
                    else:
                        age_text = f"{int(age_seconds / 60)} minutes ago"
                    metadata_items.append({"Key": "Cached", "Value": age_text})
            
            # Add any warnings
            if "warning" in conversion_data:
                st.warning(conversion_data["warning"])
            
            # Display the metadata table
            if metadata_items:
                st.write(pd.DataFrame(metadata_items))

def create_historical_chart(data: Dict[str, Any], source: str, target: str) -> go.Figure:
    """
    Create an interactive chart showing historical rates.
    
    Args:
        data: Dictionary containing lists of dates and rates
        source: Source currency code
        target: Target currency code
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    # Add main lines
    fig.add_trace(go.Scatter(
        x=data["dates"],
        y=data["rates"],
        mode='lines',
        name=f'{source} to {target}',
        line=dict(color='#1f77b4', width=2),
    ))
    
    # Add moving average if we have enough data
    if len(data["rates"]) >= 7:
        import numpy as np
        window = 7
        moving_avg = np.convolve(
            data["rates"], np.ones(window)/window, mode='valid'
        )
        
        # Adjust x values to match the length of moving_avg
        ma_dates = data["dates"][window-1:]
        
        fig.add_trace(go.Scatter(
            x=ma_dates,
            y=moving_avg,
            mode='lines',
            name=f'7-day Moving Average',
            line=dict(color='#ff7f0e', width=2, dash='dot'),
        ))
    
    # Configure layout
    fig.update_layout(
        title=f'Historical Exchange Rate: {source} to {target}',
        xaxis_title='Date',
        yaxis_title=f'Exchange Rate',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(204, 204, 204, 0.2)',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(204, 204, 204, 0.2)',
        ),
        plot_bgcolor='rgba(255, 255, 255, 0.0)',
        paper_bgcolor='rgba(255, 255, 255, 0.0)',
        margin=dict(l=10, r=10, t=60, b=10)
    )
    
    return fig

def display_rate_comparison(source: str, rates: Dict[str, float]):
    """
    Display a bar chart showing how the source currency performs against multiple targets.
    
    Args:
        source: Source currency code
        rates: Dictionary of target currencies and their rates
    """
    currencies = list(rates.keys())
    values = list(rates.values())
    
    fig = go.Figure()
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=currencies,
        y=values,
        marker_color='#1f77b4',
        text=[f"{v:.4f}" for v in values],
        textposition='auto',
    ))
    
    # Configure layout
    fig.update_layout(
        title=f'1 {source} in Other Currencies',
        xaxis_title='Currency',
        yaxis_title='Exchange Rate',
        plot_bgcolor='rgba(255, 255, 255, 0.0)',
        paper_bgcolor='rgba(255, 255, 255, 0.0)',
        margin=dict(l=10, r=10, t=40, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_audit_table(history: List[Dict[str, Any]]):
    """
    Create a table displaying conversion history for audit purposes.
    
    Args:
        history: List of dictionaries containing conversion records
    """
    if not history:
        st.info("No conversion history available yet.")
        return
    
    # Create a pandas DataFrame for better display
    df = pd.DataFrame({
        "Timestamp": [entry.get("timestamp", "") for entry in history],
        "From": [f"{entry.get('amount', 0):.2f} {entry.get('source', '')}" for entry in history],
        "To": [f"{entry.get('result', 0):.6f} {entry.get('target', '')}" for entry in history],
        "Rate": [entry.get("rate", 0) for entry in history]
    })
    
    # Format the timestamp column
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    st.dataframe(df, use_container_width=True)
    
    # Export options
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export as CSV", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="conversion_history.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        if st.button("Clear History", use_container_width=True):
            return True
    
    return False