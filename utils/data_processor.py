import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from io import BytesIO
import base64
import os

# Set style for professional charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


class DataProcessor:
    """Processes and analyzes datasets for report generation with comprehensive pattern detection"""
    
    def __init__(self, filepath):
        """Initialize with dataset filepath"""
        self.filepath = filepath
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load data from various file formats"""
        file_ext = os.path.splitext(self.filepath)[1].lower()
        
        try:
            if file_ext == '.csv':
                self.df = pd.read_csv(self.filepath)
            elif file_ext in ['.xlsx', '.xls']:
                self.df = pd.read_excel(self.filepath)
            elif file_ext == '.tsv':
                self.df = pd.read_csv(self.filepath, sep='\t')
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
            
            print(f"Successfully loaded {len(self.df)} rows and {len(self.df.columns)} columns")
        
        except Exception as e:
            raise Exception(f"Error loading file: {str(e)}")
    
    def analyze(self):
        """Perform comprehensive data analysis with pattern detection"""
        if self.df is None:
            raise ValueError("No data loaded")
        
        # Basic statistics
        total_rows = len(self.df)
        total_columns = len(self.df.columns)
        
        # Column types
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        datetime_cols = self.df.select_dtypes(include=['datetime64']).columns.tolist()
        
        # Missing values
        missing_data = self.df.isnull().sum()
        missing_percentage = (missing_data / total_rows * 100).round(2)
        
        # Enhanced Numeric summary with statistical insights
        numeric_summary = {}
        numeric_insights = []
        
        if numeric_cols:
            for col in numeric_cols:
                try:
                    col_data = self.df[col].dropna()
                    if len(col_data) == 0:
                        continue
                    
                    # Calculate statistics
                    mean_val = float(col_data.mean())
                    median_val = float(col_data.median())
                    std_val = float(col_data.std())
                    min_val = float(col_data.min())
                    max_val = float(col_data.max())
                    q1 = float(col_data.quantile(0.25))
                    q3 = float(col_data.quantile(0.75))
                    iqr = q3 - q1
                    
                    # Skewness and Kurtosis
                    skewness = float(stats.skew(col_data))
                    kurtosis = float(stats.kurtosis(col_data))
                    
                    # Outlier detection (IQR method)
                    lower_bound = q1 - 1.5 * iqr
                    upper_bound = q3 + 1.5 * iqr
                    outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                    outlier_count = len(outliers)
                    outlier_pct = (outlier_count / len(col_data) * 100)
                    
                    numeric_summary[col] = {
                        'mean': mean_val,
                        'median': median_val,
                        'std': std_val,
                        'min': min_val,
                        'max': max_val,
                        'q1': q1,
                        'q3': q3,
                        'iqr': iqr,
                        'range': max_val - min_val,
                        'coefficient_of_variation': (std_val / mean_val * 100) if mean_val != 0 else 0,
                        'skewness': skewness,
                        'kurtosis': kurtosis,
                        'outlier_count': outlier_count,
                        'outlier_percentage': outlier_pct,
                        'missing': int(missing_data[col]),
                        'missing_pct': float(missing_percentage[col])
                    }
                    
                    # Generate insights for this column
                    if abs(skewness) > 1:
                        direction = "right" if skewness > 0 else "left"
                        numeric_insights.append(f"{col} shows significant {direction}-skewed distribution (skewness: {skewness:.2f})")
                    
                    if outlier_pct > 5:
                        numeric_insights.append(f"{col} contains {outlier_count} outliers ({outlier_pct:.1f}% of data)")
                    
                    if std_val / mean_val > 1 if mean_val != 0 else False:
                        numeric_insights.append(f"{col} exhibits high variability (CV: {std_val/mean_val*100:.1f}%)")
                
                except Exception as e:
                    print(f"Error processing column {col}: {str(e)}")
                    continue
        
        # Enhanced Categorical summary with diversity analysis
        categorical_summary = {}
        categorical_insights = []
        
        if categorical_cols:
            for col in categorical_cols[:10]:
                try:
                    value_counts = self.df[col].value_counts()
                    unique_count = int(self.df[col].nunique())
                    
                    # Calculate diversity metrics
                    total_non_null = len(self.df[col].dropna())
                    if total_non_null > 0:
                        # Concentration ratio (top value percentage)
                        top_value_pct = (value_counts.iloc[0] / total_non_null * 100) if len(value_counts) > 0 else 0
                        
                        # Shannon entropy (diversity measure)
                        proportions = value_counts / total_non_null
                        entropy = -sum(proportions * np.log2(proportions + 1e-10))
                        
                        categorical_summary[col] = {
                            'unique_values': unique_count,
                            'top_values': value_counts.head(10).to_dict(),
                            'top_value_percentage': float(top_value_pct),
                            'diversity_score': float(entropy),
                            'missing': int(missing_data[col]),
                            'missing_pct': float(missing_percentage[col])
                        }
                        
                        # Generate insights
                        if top_value_pct > 50:
                            categorical_insights.append(f"{col} is dominated by '{value_counts.index[0]}' ({top_value_pct:.1f}%)")
                        
                        if unique_count == total_non_null:
                            categorical_insights.append(f"{col} appears to be a unique identifier (all values unique)")
                        elif unique_count < 10:
                            categorical_insights.append(f"{col} has low cardinality ({unique_count} unique values)")
                
                except Exception as e:
                    print(f"Error processing categorical column {col}: {str(e)}")
                    continue
        
        # Advanced Correlations with strength classification
        correlations = []
        correlation_insights = []
        
        if len(numeric_cols) > 1:
            corr_matrix = self.df[numeric_cols].corr()
            corr_pairs = []
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = float(corr_matrix.iloc[i, j])
                    if not np.isnan(corr_val):
                        corr_pairs.append({
                            'var1': corr_matrix.columns[i],
                            'var2': corr_matrix.columns[j],
                            'correlation': corr_val,
                            'strength': self._classify_correlation(corr_val)
                        })
            
            # Sort by absolute correlation
            corr_pairs.sort(key=lambda x: abs(x['correlation']), reverse=True)
            correlations = corr_pairs[:10]
            
            # Generate correlation insights
            strong_correlations = [c for c in corr_pairs if abs(c['correlation']) > 0.7]
            if strong_correlations:
                for corr in strong_correlations[:3]:
                    direction = "positive" if corr['correlation'] > 0 else "negative"
                    correlation_insights.append(
                        f"Strong {direction} correlation between {corr['var1']} and {corr['var2']} (r={corr['correlation']:.3f})"
                    )
        
        # Data Quality Assessment
        quality_score = self._calculate_quality_score(missing_percentage, total_rows)
        
        # Automatically determine analysis type
        analysis_type = self._determine_analysis_type(numeric_cols, categorical_cols, total_rows)
        
        summary = {
            'total_rows': total_rows,
            'total_columns': total_columns,
            'numeric_columns': len(numeric_cols),
            'categorical_columns': len(categorical_cols),
            'datetime_columns': len(datetime_cols),
            'column_names': self.df.columns.tolist(),
            'numeric_column_names': numeric_cols,
            'categorical_column_names': categorical_cols,
            'numeric_summary': numeric_summary,
            'categorical_summary': categorical_summary,
            'correlations': correlations,
            'data_sample': self.df.head(5).to_dict('records'),
            # Enhanced insights
            'numeric_insights': numeric_insights,
            'categorical_insights': categorical_insights,
            'correlation_insights': correlation_insights,
            'data_quality_score': quality_score,
            'recommended_analysis_type': analysis_type,
            'missing_data_summary': {
                'columns_with_missing': int(missing_data[missing_data > 0].count()),
                'total_missing_cells': int(missing_data.sum()),
                'missing_percentage': float((missing_data.sum() / (total_rows * total_columns) * 100))
            }
        }
        
        return summary
    
    def _classify_correlation(self, corr_val):
        """Classify correlation strength"""
        abs_corr = abs(corr_val)
        if abs_corr >= 0.9:
            return "Very Strong"
        elif abs_corr >= 0.7:
            return "Strong"
        elif abs_corr >= 0.5:
            return "Moderate"
        elif abs_corr >= 0.3:
            return "Weak"
        else:
            return "Very Weak"
    
    def _calculate_quality_score(self, missing_percentage, total_rows):
        """Calculate overall data quality score (0-100)"""
        # Factors: completeness, sample size
        completeness_score = 100 - missing_percentage.mean()
        
        # Sample size score (logarithmic scale)
        if total_rows < 100:
            size_score = 50
        elif total_rows < 1000:
            size_score = 70
        elif total_rows < 10000:
            size_score = 85
        else:
            size_score = 100
        
        # Weighted average
        quality_score = (completeness_score * 0.6) + (size_score * 0.4)
        return round(quality_score, 1)
    
    def _determine_analysis_type(self, numeric_cols, categorical_cols, total_rows):
        """Automatically determine the best analysis approach"""
        if len(numeric_cols) > 5 and len(categorical_cols) > 2:
            return "Mixed Analysis (Multivariate with Segmentation)"
        elif len(numeric_cols) > 3:
            return "Quantitative Analysis (Statistical & Correlation)"
        elif len(categorical_cols) > 5:
            return "Categorical Analysis (Frequency & Distribution)"
        elif total_rows > 10000:
            return "Large-Scale Descriptive Analysis"
        else:
            return "Exploratory Data Analysis (EDA)"
    
    def generate_charts(self):
        """Generate intelligent visualizations with interpretations"""
        charts = []
        
        # For large datasets, sample to improve performance
        df_sample = self.df
        if len(self.df) > 10000:
            print(f"Large dataset detected ({len(self.df)} rows). Sampling 10,000 rows for visualization.")
            df_sample = self.df.sample(n=10000, random_state=42)
        
        numeric_cols = df_sample.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df_sample.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Chart 1: Distribution Analysis with interpretation
        if numeric_cols:
            fig, ax = plt.subplots(figsize=(10, 6))
            col = numeric_cols[0]
            col_data = df_sample[col].dropna()
            
            n, bins, patches = ax.hist(col_data, bins=30, edgecolor='black', alpha=0.7, color='steelblue')
            
            # Add mean and median lines
            mean_val = col_data.mean()
            median_val = col_data.median()
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
            
            ax.set_title(f'Distribution Analysis: {col}', fontsize=14, fontweight='bold')
            ax.set_xlabel(col, fontsize=12)
            ax.set_ylabel('Frequency', fontsize=12)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Interpretation
            skewness = stats.skew(col_data)
            interpretation = f"Distribution is {'right-skewed' if skewness > 0.5 else 'left-skewed' if skewness < -0.5 else 'approximately symmetric'}"
            
            charts.append({
                'title': f'Distribution Analysis: {col}',
                'image': self._fig_to_base64(fig),
                'path': self._save_chart(fig, f'distribution_{col}'),
                'interpretation': interpretation
            })
            plt.close(fig)
        
        # Chart 2: Enhanced Correlation heatmap with annotations
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots(figsize=(12, 10))
            corr = df_sample[numeric_cols[:10]].corr()
            
            # Create mask for upper triangle
            mask = np.triu(np.ones_like(corr, dtype=bool))
            
            sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='coolwarm', 
                       center=0, ax=ax, cbar_kws={'label': 'Correlation Coefficient'},
                       square=True, linewidths=0.5)
            ax.set_title('Correlation Matrix (Lower Triangle)', fontsize=14, fontweight='bold')
            plt.tight_layout()
            
            # Find strongest correlation
            corr_no_diag = corr.where(~np.eye(corr.shape[0], dtype=bool))
            max_corr = corr_no_diag.max().max()
            max_pair = corr_no_diag.stack().idxmax()
            
            interpretation = f"Strongest correlation: {max_pair[0]} vs {max_pair[1]} (r={max_corr:.3f})"
            
            charts.append({
                'title': 'Correlation Matrix Analysis',
                'image': self._fig_to_base64(fig),
                'path': self._save_chart(fig, 'correlation_heatmap'),
                'interpretation': interpretation
            })
            plt.close(fig)
        
        # Chart 3: Top Categories with percentage labels
        if categorical_cols:
            col = categorical_cols[0]
            value_counts = df_sample[col].value_counts().head(10)
            percentages = (value_counts / len(df_sample) * 100)
            
            fig, ax = plt.subplots(figsize=(12, 6))
            bars = ax.bar(range(len(value_counts)), value_counts.values, color='steelblue', edgecolor='black')
            
            # Add percentage labels on bars
            for i, (bar, pct) in enumerate(zip(bars, percentages)):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)
            
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
            ax.set_title(f'Top 10 Categories: {col}', fontsize=14, fontweight='bold')
            ax.set_xlabel(col, fontsize=12)
            ax.set_ylabel('Count', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            
            interpretation = f"Top category '{value_counts.index[0]}' represents {percentages.iloc[0]:.1f}% of data"
            
            charts.append({
                'title': f'Category Distribution: {col}',
                'image': self._fig_to_base64(fig),
                'path': self._save_chart(fig, f'bar_{col}'),
                'interpretation': interpretation
            })
            plt.close(fig)
        
        # Chart 4: Box Plot with outlier analysis
        if len(numeric_cols) >= 2:
            fig, ax = plt.subplots(figsize=(12, 6))
            cols_to_plot = numeric_cols[:5]
            df_sample[cols_to_plot].boxplot(ax=ax, patch_artist=True,
                                            boxprops=dict(facecolor='lightblue'),
                                            medianprops=dict(color='red', linewidth=2))
            ax.set_title('Box Plot Analysis - Outlier Detection', fontsize=14, fontweight='bold')
            ax.set_ylabel('Value', fontsize=12)
            ax.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Count outliers
            outlier_counts = []
            for col in cols_to_plot:
                q1 = df_sample[col].quantile(0.25)
                q3 = df_sample[col].quantile(0.75)
                iqr = q3 - q1
                outliers = df_sample[col][(df_sample[col] < q1 - 1.5*iqr) | (df_sample[col] > q3 + 1.5*iqr)]
                outlier_counts.append(len(outliers))
            
            max_outliers = max(outlier_counts)
            max_col = cols_to_plot[outlier_counts.index(max_outliers)]
            interpretation = f"{max_col} shows the most outliers ({max_outliers} data points)"
            
            charts.append({
                'title': 'Box Plot - Outlier Analysis',
                'image': self._fig_to_base64(fig),
                'path': self._save_chart(fig, 'boxplot'),
                'interpretation': interpretation
            })
            plt.close(fig)
        
        # Chart 5: Scatter plot for top correlated variables
        if len(numeric_cols) >= 2:
            corr_matrix = df_sample[numeric_cols].corr()
            # Find highest correlation pair
            corr_no_diag = corr_matrix.where(~np.eye(corr_matrix.shape[0], dtype=bool))
            if not corr_no_diag.isna().all().all():
                max_corr_val = abs(corr_no_diag).max().max()
                max_pair = abs(corr_no_diag).stack().idxmax()
                
                fig, ax = plt.subplots(figsize=(10, 6))
                x_col, y_col = max_pair[0], max_pair[1]
                
                ax.scatter(df_sample[x_col], df_sample[y_col], alpha=0.5, color='steelblue')
                
                # Add trend line
                z = np.polyfit(df_sample[x_col].dropna(), df_sample[y_col].dropna(), 1)
                p = np.poly1d(z)
                ax.plot(df_sample[x_col], p(df_sample[x_col]), "r--", linewidth=2, label='Trend Line')
                
                ax.set_title(f'Relationship: {x_col} vs {y_col}', fontsize=14, fontweight='bold')
                ax.set_xlabel(x_col, fontsize=12)
                ax.set_ylabel(y_col, fontsize=12)
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                
                corr_val = corr_matrix.loc[x_col, y_col]
                direction = "positive" if corr_val > 0 else "negative"
                interpretation = f"{direction.capitalize()} correlation (r={corr_val:.3f}) - as {x_col} increases, {y_col} tends to {'increase' if corr_val > 0 else 'decrease'}"
                
                charts.append({
                    'title': f'Scatter Plot: {x_col} vs {y_col}',
                    'image': self._fig_to_base64(fig),
                    'path': self._save_chart(fig, 'scatter_correlation'),
                    'interpretation': interpretation
                })
                plt.close(fig)
        
        return charts
    
    def _fig_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        buffer.close()
        return image_base64
    
    def _save_chart(self, fig, name):
        """Save chart to file and return path"""
        os.makedirs('outputs/charts', exist_ok=True)
        path = f'outputs/charts/{name}.png'
        fig.savefig(path, dpi=150, bbox_inches='tight')
        return path
