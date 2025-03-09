import plotly.graph_objects as go
import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import datetime

def create_rate_chart(rate_data: List[Dict[str, Any]], source: str, target: str) -> go.Figure:
    """
    Create an interactive line chart showing exchange rate trends with enhanced visuals.
    
    Args:
        rate_data: List of dictionaries with date and rate information
        source: Source currency code
        target: Target currency code
        
    Returns:
        Plotly figure object
    """
    from ui.styles import get_currency_color
    
    dates = [entry["date"] for entry in rate_data]
    rates = [entry["rate"] for entry in rate_data]
    
    # Get colors based on currencies
    source_color = get_currency_color(source)
    target_color = get_currency_color(target)
    
    # Create gradient colors for the chart
    main_color = source_color
    secondary_color = target_color
    
    # Check if dark mode is active
    is_dark_mode = False
    if "theme" in st.session_state and st.session_state.theme == "Dark":
        is_dark_mode = True
    
    # Set background and text colors based on theme
    bg_color = "rgba(25, 38, 85, 0.0)" if is_dark_mode else "rgba(255, 255, 255, 0.0)"
    text_color = "#F5F7FF" if is_dark_mode else "#333333"
    grid_color = "rgba(255, 255, 255, 0.1)" if is_dark_mode else "rgba(204, 204, 204, 0.2)"
    annotation_bg = "rgba(25, 38, 85, 0.8)" if is_dark_mode else "rgba(255, 255, 255, 0.8)"
    
    fig = go.Figure()
    
    # Add area under the line for visual appeal
    fig.add_trace(go.Scatter(
        x=dates,
        y=rates,
        fill='tozeroy',
        fillcolor=f'rgba({int(main_color[1:3], 16)}, {int(main_color[3:5], 16)}, {int(main_color[5:7], 16)}, 0.1)',
        line=dict(width=0),
        showlegend=False
    ))
    
    # Add main line with gradient effect
    fig.add_trace(go.Scatter(
        x=dates,
        y=rates,
        mode='lines+markers',
        name=f'{source} to {target}',
        line=dict(color=main_color, width=3, shape='spline'),
        marker=dict(
            size=10,
            color=main_color,
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>Date:</b> %{x}<br><b>Rate:</b> %{y:.6f}<extra></extra>'
    ))
    
    # Calculate min and max for range with more padding for visual appeal
    min_rate = min(rates) * 0.92
    max_rate = max(rates) * 1.08
    
    # Configure layout with enhanced styling
    fig.update_layout(
        title={
            'text': f'<b>{source}</b> to <b>{target}</b> Exchange Rate Trend',
            'font': {'size': 24, 'color': text_color},
            'y': 0.95
        },
        xaxis_title='<b>Date</b>',
        yaxis_title=f'<b>Exchange Rate</b> (1 {source} in {target})',
        hovermode='x unified',
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            tickfont={'size': 12, 'color': text_color},
            title_font={'size': 14, 'color': text_color}
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            range=[min_rate, max_rate],
            tickfont={'size': 12, 'color': text_color},
            title_font={'size': 14, 'color': text_color},
            tickformat='.6f'
        ),
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            bgcolor=annotation_bg,
            bordercolor='rgba(0, 0, 0, 0.1)',
            borderwidth=1,
            font=dict(color=text_color)
        ),
        hoverlabel=dict(
            bgcolor=annotation_bg,
            font_size=14,
            bordercolor=main_color
        ),
        # Add animation effect
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(
                        label='Play Animation',
                        method='animate',
                        args=[None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]
                    )
                ],
                x=0.1,
                y=1.1,
                visible=False
            )
        ]
    )
    
    # Add current rate line with enhanced styling
    current_rate = rates[-1]
    fig.add_shape(
        type="line",
        x0=dates[0],
        y0=current_rate,
        x1=dates[-1],
        y1=current_rate,
        line=dict(
            color=secondary_color,
            width=2,
            dash="dash",
        )
    )
    
    # Add annotation for latest rate with enhanced styling
    fig.add_annotation(
        x=dates[-1],
        y=current_rate,
        text=f"<b>Current:</b> {current_rate:.6f}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowcolor=secondary_color,
        arrowwidth=2,
        bgcolor=annotation_bg,
        bordercolor=secondary_color,
        borderwidth=2,
        borderpad=4,
        font=dict(color=secondary_color, size=14)
    )
    
    # Add min/max indicators
    max_rate_value = max(rates)
    max_rate_date = dates[rates.index(max_rate_value)]
    min_rate_value = min(rates)
    min_rate_date = dates[rates.index(min_rate_value)]
    
    # Add max point annotation
    fig.add_annotation(
        x=max_rate_date,
        y=max_rate_value,
        text=f"High: {max_rate_value:.6f}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowcolor='#00C897',
        arrowwidth=1.5,
        bgcolor=annotation_bg,
        bordercolor='#00C897',
        borderwidth=1.5,
        borderpad=3,
        font=dict(color='#00C897', size=12),
        yshift=20
    )
    
    # Add min point annotation
    fig.add_annotation(
        x=min_rate_date,
        y=min_rate_value,
        text=f"Low: {min_rate_value:.6f}",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowcolor='#FF5757',
        arrowwidth=1.5,
        bgcolor=annotation_bg,
        bordercolor='#FF5757',
        borderwidth=1.5,
        borderpad=3,
        font=dict(color='#FF5757', size=12),
        yshift=-20
    )
    
    return fig

def display_conversion_metadata(conversion_data: Dict[str, Any]):
    """
    Display metadata about a conversion in a formatted panel with enhanced visuals.
    
    Args:
        conversion_data: Dictionary containing conversion metadata
    """
    from ui.styles import get_currency_color
    
    # Get currency colors
    source_color = get_currency_color(conversion_data.get('source', 'USD'))
    target_color = get_currency_color(conversion_data.get('target', 'BTC'))
    
    # Create a visually appealing header with gradient
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, {source_color}, {target_color});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    ">
        Conversion Details
    </div>
    """, unsafe_allow_html=True)
    
    # Create a card-like container with animation
    st.markdown("""
    <style>
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .metadata-container {
        animation: slideUp 0.6s ease-out forwards;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    </style>
    <div class="metadata-container"></div>
    """, unsafe_allow_html=True)
    
    # Create a visually appealing container
    with st.container():
        col1, col2 = st.columns(2)
        
        with col1:
            # Enhanced metric display
            rate = conversion_data['rate']
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba({int(source_color[1:3], 16)}, {int(source_color[3:5], 16)}, {int(source_color[5:7], 16)}, 0.1), 
                                          rgba({int(target_color[1:3], 16)}, {int(target_color[3:5], 16)}, {int(target_color[5:7], 16)}, 0.1));
                border-radius: 12px;
                padding: 1rem;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                text-align: center;
            ">
                <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">Exchange Rate</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #333;">{rate:.6f}</div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 0.5rem;">1 {conversion_data.get('source', 'USD')} = {rate:.6f} {conversion_data.get('target', 'BTC')}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Format the timestamp with enhanced styling
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
            
            st.markdown(f"""
            <div style="
                background: rgba(5, 191, 219, 0.1);
                border-left: 4px solid #05BFDB;
                border-radius: 4px;
                padding: 0.8rem;
                margin-top: 1rem;
                display: flex;
                align-items: center;
            ">
                <div style="font-size: 1.5rem; margin-right: 0.8rem;">📅</div>
                <div>
                    <div style="font-size: 0.8rem; color: #666;">Last Updated</div>
                    <div style="font-weight: 600; color: #333;">{formatted_time}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            # Create a metadata table with enhanced styling
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
            
            # Add any warnings with enhanced styling
            if "warning" in conversion_data:
                st.markdown(f"""
                <div style="
                    background: rgba(255, 177, 0, 0.1);
                    border-left: 4px solid #FFB100;
                    border-radius: 4px;
                    padding: 0.8rem;
                    margin-bottom: 1rem;
                    display: flex;
                    align-items: center;
                ">
                    <div style="font-size: 1.5rem; margin-right: 0.8rem;">⚠️</div>
                    <div style="color: #333;">{conversion_data["warning"]}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Display the metadata table with enhanced styling
            if metadata_items:
                # Create a styled table header
                st.markdown("""
                <div style="
                    font-weight: 600;
                    margin-bottom: 0.5rem;
                    color: #6236FF;
                    font-size: 0.9rem;
                ">
                    Additional Information
                </div>
                """, unsafe_allow_html=True)
                
                # Create a custom styled table
                table_html = """
                <div style="
                    background: rgba(255, 255, 255, 0.5);
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
                    font-size: 0.9rem;
                ">
                    <table style="width: 100%; border-collapse: collapse;">
                """
                
                for item in metadata_items:
                    table_html += f"""
                    <tr style="border-bottom: 1px solid rgba(0, 0, 0, 0.05);">
                        <td style="padding: 0.6rem; color: #666; font-weight: 600;">{item['Key']}</td>
                        <td style="padding: 0.6rem; color: #333;">{item['Value']}</td>
                    </tr>
                    """
                
                table_html += """
                    </table>
                </div>
                """
                
                st.markdown(table_html, unsafe_allow_html=True)

def create_historical_chart(data: Dict[str, Any], source: str, target: str) -> go.Figure:
    """
    Create an interactive chart showing historical rates with enhanced visuals.
    
    Args:
        data: Dictionary containing lists of dates and rates
        source: Source currency code
        target: Target currency code
        
    Returns:
        Plotly figure object
    """
    from ui.styles import get_currency_color
    
    # Get colors based on currencies
    source_color = get_currency_color(source)
    target_color = get_currency_color(target)
    
    fig = go.Figure()
    
    # Add area under the line for visual appeal
    fig.add_trace(go.Scatter(
        x=data["dates"],
        y=data["rates"],
        fill='tozeroy',
        fillcolor=f'rgba({int(source_color[1:3], 16)}, {int(source_color[3:5], 16)}, {int(source_color[5:7], 16)}, 0.1)',
        line=dict(width=0),
        showlegend=False
    ))
    
    # Add main line with enhanced styling
    fig.add_trace(go.Scatter(
        x=data["dates"],
        y=data["rates"],
        mode='lines',
        name=f'{source} to {target}',
        line=dict(color=source_color, width=3, shape='spline'),
        hovertemplate='<b>Date:</b> %{x}<br><b>Rate:</b> %{y:.6f}<extra></extra>'
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
            line=dict(color=target_color, width=2, dash='dot'),
            hovertemplate='<b>Date:</b> %{x}<br><b>Average:</b> %{y:.6f}<extra></extra>'
        ))
    
    # Calculate min and max for range with more padding for visual appeal
    min_rate = min(data["rates"]) * 0.92
    max_rate = max(data["rates"]) * 1.08
    
    # Configure layout with enhanced styling
    fig.update_layout(
        title={
            'text': f'<b>Historical Exchange Rate:</b> {source} to {target}',
            'font': {'size': 24, 'color': '#333333'},
            'y': 0.95
        },
        xaxis_title='<b>Date</b>',
        yaxis_title='<b>Exchange Rate</b>',
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255, 255, 255, 0.5)',
            bordercolor='rgba(0, 0, 0, 0.1)',
            borderwidth=1
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(204, 204, 204, 0.2)',
            tickfont={'size': 12},
            title_font={'size': 14}
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(204, 204, 204, 0.2)',
            range=[min_rate, max_rate],
            tickfont={'size': 12},
            title_font={'size': 14},
            tickformat='.6f'
        ),
        plot_bgcolor='rgba(255, 255, 255, 0.0)',
        paper_bgcolor='rgba(255, 255, 255, 0.0)',
        margin=dict(l=10, r=10, t=60, b=10),
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            bordercolor=source_color
        ),
        # Add animation effect
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(
                        label='Play Animation',
                        method='animate',
                        args=[None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}]
                    )
                ],
                x=0.1,
                y=1.1,
                visible=False
            )
        ]
    )
    
    # Add trend indicators
    if len(data["rates"]) > 1:
        first_rate = data["rates"][0]
        last_rate = data["rates"][-1]
        percent_change = ((last_rate - first_rate) / first_rate) * 100
        
        trend_color = "#00C897" if percent_change >= 0 else "#FF5757"
        trend_icon = "↗" if percent_change >= 0 else "↘"
        
        fig.add_annotation(
            x=0.02,
            y=0.98,
            xref="paper",
            yref="paper",
            text=f"<b>Trend:</b> {trend_icon} {abs(percent_change):.2f}%",
            showarrow=False,
            font=dict(size=14, color=trend_color),
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor=trend_color,
            borderwidth=2,
            borderpad=4,
            align="left"
        )
    
    return fig

def display_rate_comparison(source: str, rates: Dict[str, float]):
    """
    Display a bar chart showing how the source currency performs against multiple targets with enhanced visuals.
    
    Args:
        source: Source currency code
        rates: Dictionary of target currencies and their rates
    """
    from ui.styles import get_currency_color, apply_currency_icons
    
    currencies = list(rates.keys())
    values = list(rates.values())
    
    # Get currency icons
    currency_icons = apply_currency_icons()
    
    # Create custom labels with icons
    labels = [f"{currency_icons.get(curr, '💱')} {curr}" for curr in currencies]
    
    # Get colors for each currency
    colors = [get_currency_color(curr) for curr in currencies]
    
    fig = go.Figure()
    
    # Add bar chart with gradient colors and hover effects
    fig.add_trace(go.Bar(
        x=labels,
        y=values,
        marker=dict(
            color=colors,
            opacity=0.8,
            line=dict(width=1, color='rgba(255, 255, 255, 0.5)')
        ),
        text=[f"{v:.6f}" for v in values],
        textposition='auto',
        textfont=dict(color='white', size=12),
        hovertemplate='<b>%{x}</b><br>Rate: %{y:.6f}<extra></extra>'
    ))
    
    # Configure layout with enhanced styling
    fig.update_layout(
        title={
            'text': f'<b>1 {source}</b> in Other Currencies',
            'font': {'size': 24, 'color': '#333333'},
            'y': 0.95
        },
        xaxis_title='<b>Currency</b>',
        yaxis_title='<b>Exchange Rate</b>',
        plot_bgcolor='rgba(255, 255, 255, 0.0)',
        paper_bgcolor='rgba(255, 255, 255, 0.0)',
        margin=dict(l=10, r=10, t=60, b=10),
        xaxis=dict(
            tickfont={'size': 12},
            title_font={'size': 14}
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(204, 204, 204, 0.2)',
            tickfont={'size': 12},
            title_font={'size': 14},
            tickformat='.6f'
        ),
        hoverlabel=dict(
            bgcolor='white',
            font_size=14,
            bordercolor=get_currency_color(source)
        )
    )
    
    # Add animation
    st.markdown("""
    <style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .rate-comparison-container {
        animation: fadeInUp 0.8s ease-out forwards;
    }
    </style>
    <div class="rate-comparison-container"></div>
    """, unsafe_allow_html=True)
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def create_audit_table(history: List[Dict[str, Any]]):
    """
    Create a table displaying conversion history for audit purposes with enhanced visuals.
    
    Args:
        history: List of dictionaries containing conversion records
    """
    from ui.styles import get_currency_color, apply_currency_icons
    
    # Add animation for the container
    st.markdown("""
    <style>
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .audit-table-container {
        animation: fadeInUp 0.8s ease-out forwards;
    }
    </style>
    <div class="audit-table-container"></div>
    """, unsafe_allow_html=True)
    
    if not history:
        st.markdown("""
        <div style="
            background: rgba(5, 191, 219, 0.1);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        ">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <div style="font-weight: 600; color: #05BFDB; margin-bottom: 0.5rem;">No Conversion History</div>
            <div style="color: #666; font-size: 0.9rem;">Convert currencies to see your history here</div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Create a visually appealing header
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #6236FF, #05BFDB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    ">
        <span style="margin-right: 10px;">📝</span> Conversion History
    </div>
    """, unsafe_allow_html=True)
    
    # Create a pandas DataFrame for better display
    df = pd.DataFrame({
        "Timestamp": [entry.get("timestamp", "") for entry in history],
        "From": [f"{entry.get('amount', 0):.2f} {entry.get('source', '')}" for entry in history],
        "To": [f"{entry.get('result', 0):.6f} {entry.get('target', '')}" for entry in history],
        "Rate": [entry.get("rate", 0) for entry in history],
        "Source": [entry.get('source', '') for entry in history],
        "Target": [entry.get('target', '') for entry in history]
    })
    
    # Format the timestamp column
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')
    df["Timestamp"] = df["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the Rate column
    df["Rate"] = df["Rate"].apply(lambda x: f"{x:.6f}")
    
    # Get currency icons
    currency_icons = apply_currency_icons()
    
    # Add styling to the dataframe
    st.markdown("""
    <style>
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    [data-testid="stDataFrame"] table {
        border-collapse: separate;
        border-spacing: 0;
    }
    [data-testid="stDataFrame"] th {
        background: linear-gradient(90deg, rgba(98, 54, 255, 0.1), rgba(5, 191, 219, 0.1));
        color: #333;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
    }
    [data-testid="stDataFrame"] td {
        transition: all 0.3s ease;
    }
    [data-testid="stDataFrame"] tr:hover td {
        background-color: rgba(98, 54, 255, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the styled dataframe
    st.dataframe(
        df[["Timestamp", "From", "To", "Rate"]], 
        use_container_width=True,
        hide_index=True
    )
    
    # Add a summary card with stats
    if len(history) > 1:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            most_converted = df['Source'].value_counts().idxmax()
            icon = currency_icons.get(most_converted, '💱')
            color = get_currency_color(most_converted)
            
            st.markdown(f"""
            <div style="
                background: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1);
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                height: 100%;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 0.8rem; color: #666;">Most Converted From</div>
                <div style="font-weight: 700; color: {color};">{most_converted}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            most_target = df['Target'].value_counts().idxmax()
            icon = currency_icons.get(most_target, '💱')
            color = get_currency_color(most_target)
            
            st.markdown(f"""
            <div style="
                background: rgba({int(color[1:3], 16)}, {int(color[3:5], 16)}, {int(color[5:7], 16)}, 0.1);
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                height: 100%;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <div style="font-size: 0.8rem; color: #666;">Most Converted To</div>
                <div style="font-weight: 700; color: {color};">{most_target}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            total_conversions = len(history)
            
            st.markdown(f"""
            <div style="
                background: rgba(98, 54, 255, 0.1);
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                height: 100%;
            ">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🔄</div>
                <div style="font-size: 0.8rem; color: #666;">Total Conversions</div>
                <div style="font-weight: 700; color: #6236FF;">{total_conversions}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Export options with enhanced styling
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export as CSV", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="conversion_history.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            return True
    
    return False