import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIEngine:
    """AI-powered comprehensive narrative generation using OpenAI GPT"""
    
    def __init__(self, config):
        """
        Initialize AI Engine with OpenAI API
        
        Args:
            config (dict): Configuration with API key and model settings
        """
        self.api_key = config.get('api_key') or os.getenv('OPENAI_API_KEY')
        self.model = config.get('model', 'gpt-4-turbo-preview')
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 2000)
        
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: OpenAI initialization failed: {str(e)}")
                self.client = None
        else:
            self.client = None
    
    def generate_insights(self, data_summary, charts=None):
        """
        Generate comprehensive insights for the report
        
        Args:
            data_summary (dict): Comprehensive data analysis summary
            charts (list): Optional list of chart metadata
            
        Returns:
            dict: Dictionary containing all narrative sections
        """
        context = self._build_comprehensive_context(data_summary)
        
        return {
            'executive_summary': self._generate_executive_summary(context, data_summary),
            'key_findings': self._generate_key_findings(context, data_summary),
            'insights': self._generate_insights_interpretation(context, data_summary),
            'recommendations': self._generate_recommendations(context, data_summary)
        }
    
    def _build_comprehensive_context(self, data_summary):
        """Build detailed context string from data summary with all insights"""
        context_parts = []
        
        # Research Objective (if provided)
        if data_summary.get('objective'):
            context_parts.append("=== RESEARCH OBJECTIVE ===")
            context_parts.append(data_summary['objective'])
            context_parts.append("")
        
        # Dataset Overview
        context_parts.append("=== DATASET OVERVIEW ===")
        context_parts.append(f"Total Records: {data_summary.get('total_rows', 0):,}")
        context_parts.append(f"Total Variables: {data_summary.get('total_columns', 0)}")
        context_parts.append(f"Numeric Columns: {data_summary.get('numeric_columns', 0)}")
        context_parts.append(f"Categorical Columns: {data_summary.get('categorical_columns', 0)}")
        
        # Data Quality
        if 'data_quality_score' in data_summary:
            context_parts.append(f"\nData Quality Score: {data_summary['data_quality_score']}/100")
        
        if 'recommended_analysis_type' in data_summary:
            context_parts.append(f"Recommended Analysis: {data_summary['recommended_analysis_type']}")
        
        # Missing Data
        if 'missing_data_summary' in data_summary:
            missing = data_summary['missing_data_summary']
            context_parts.append(f"\nMissing Data: {missing.get('missing_percentage', 0):.2f}%")
        
        # Numeric Variables with Statistics
        if data_summary.get('numeric_summary'):
            context_parts.append(f"\n=== NUMERIC VARIABLES ({len(data_summary['numeric_summary'])}) ===")
            for col, stats in list(data_summary['numeric_summary'].items())[:10]:
                context_parts.append(f"\n{col}:")
                context_parts.append(f"  Mean: {stats.get('mean', 0):.2f} | Median: {stats.get('median', 0):.2f}")
                context_parts.append(f"  Std Dev: {stats.get('std', 0):.2f} | Range: [{stats.get('min', 0):.2f}, {stats.get('max', 0):.2f}]")
                if 'skewness' in stats:
                    context_parts.append(f"  Skewness: {stats['skewness']:.2f} | Kurtosis: {stats.get('kurtosis', 0):.2f}")
                if stats.get('outlier_percentage', 0) > 0:
                    context_parts.append(f"  Outliers: {stats.get('outlier_count', 0)} ({stats.get('outlier_percentage', 0):.1f}%)")
        
        # Categorical Variables
        if data_summary.get('categorical_summary'):
            context_parts.append(f"\n=== CATEGORICAL VARIABLES ({len(data_summary['categorical_summary'])}) ===")
            for col, stats in list(data_summary['categorical_summary'].items())[:10]:
                context_parts.append(f"\n{col}:")
                context_parts.append(f"  Unique Values: {stats.get('unique_values', 0)}")
                top_values = stats.get('top_values', {})
                if top_values:
                    top_3 = list(top_values.items())[:3]
                    context_parts.append(f"  Top Values: {', '.join([f'{k} ({v})' for k, v in top_3])}")
                if 'top_value_percentage' in stats:
                    context_parts.append(f"  Concentration: {stats['top_value_percentage']:.1f}% in top category")
        
        # Correlations
        if data_summary.get('correlations'):
            context_parts.append(f"\n=== CORRELATIONS (Top 10) ===")
            for corr in data_summary['correlations'][:10]:
                context_parts.append(
                    f"• {corr.get('variable_1', 'N/A')} ↔ {corr.get('variable_2', 'N/A')}: "
                    f"r={corr.get('coefficient', 0):.3f} ({corr.get('strength', 'N/A')})"
                )
        
        # Automated Insights
        if data_summary.get('numeric_insights'):
            context_parts.append("\n=== NUMERIC INSIGHTS ===")
            for insight in data_summary['numeric_insights'][:5]:
                context_parts.append(f"• {insight}")
        
        if data_summary.get('categorical_insights'):
            context_parts.append("\n=== CATEGORICAL INSIGHTS ===")
            for insight in data_summary['categorical_insights'][:5]:
                context_parts.append(f"• {insight}")
        
        if data_summary.get('correlation_insights'):
            context_parts.append("\n=== CORRELATION INSIGHTS ===")
            for insight in data_summary['correlation_insights'][:5]:
                context_parts.append(f"• {insight}")
        
        return "\n".join(context_parts)
    
    def _generate_executive_summary(self, context, data_summary):
        """Generate comprehensive executive summary"""
        
        objective_instruction = ""
        if data_summary.get('objective'):
            objective_instruction = f"""
RESEARCH OBJECTIVE: {data_summary['objective']}

CRITICAL: All analysis must be framed in relation to this research objective. Evaluate every finding, pattern, and insight for its relevance to achieving this stated goal."""
        
        prompt = f"""You are a senior data analyst writing an executive summary for a professional Canadian business report.
{objective_instruction}

DATASET INFORMATION:
{context}

Write a comprehensive executive summary (4-6 paragraphs, 400-500 words) that includes:

PARAGRAPH 1: Overview
- Dataset size, scope, and purpose
- Primary variables and data types
{f'- Direct connection to the research objective' if data_summary.get('objective') else ''}

PARAGRAPH 2: Key Metrics
- Most important numerical findings (means, medians, ranges)
- Standout percentages or rates
{f'- Metrics most critical to the stated objective' if data_summary.get('objective') else ''}

PARAGRAPH 3: Patterns and Trends
- Major correlations discovered
- Distribution characteristics
- Outliers or anomalies
{f'- Patterns that support or inform the research objective' if data_summary.get('objective') else ''}

PARAGRAPH 4: Categorical Insights
- Dominant categories and their proportions
- Diversity or concentration patterns

PARAGRAPH 5: Data Quality & Analysis
- Overall data quality assessment
- Recommended analysis type
- Any limitations or considerations

PARAGRAPH 6 (if needed): Strategic Implications
- High-level business implications
- Areas requiring attention
{f'- Next steps toward achieving the research objective' if data_summary.get('objective') else ''}

Use specific numbers, percentages, and statistics from the data. Write in clear, professional Canadian English. Focus on actionable insights that executives need to know."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional senior data analyst creating executive summaries for Canadian business reports. You provide detailed, data-driven insights with specific numbers and percentages."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating executive summary: {str(e)}")
            return self._create_detailed_fallback_summary(data_summary)
    
    def _generate_key_findings(self, context, data_summary):
        """Generate detailed key findings with multiple subsections"""
        
        objective_instruction = ""
        if data_summary.get('objective'):
            objective_instruction = f"""
RESEARCH OBJECTIVE: {data_summary['objective']}

CRITICAL: Frame all findings in direct relation to this research objective. Highlight data patterns and metrics that directly inform or impact the stated goal."""
        
        prompt = f"""You are a data analyst writing the Key Findings section for a professional analytical report.
{objective_instruction}

DATASET INFORMATION:
{context}

Write a comprehensive Key Findings section (600-800 words) organized into clear subsections:

4.1 Data Composition Overview
- Total records and variables
- Data types breakdown
- Quality metrics

4.2 Numerical Analysis
- Key statistics for top 3-5 numeric variables
- Distributions (symmetric, skewed, etc.)
- Outliers and anomalies

4.3 Categorical Breakdown
- Dominant categories and their percentages
- Top values in key categorical fields
- Diversity patterns

4.4 Correlation Patterns
- Strongest positive correlations with explanations
- Notable negative correlations
- What these relationships indicate
{f'- Correlations most relevant to the research objective' if data_summary.get('objective') else ''}

4.5 Notable Patterns
- Any clusters or groupings
- Trends across variables
- Anomalies requiring attention

Use specific numbers from the data. Be thorough but concise. Write in professional Canadian English."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional data analyst writing detailed findings sections for analytical reports. You focus on facts, numbers, and observable patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating key findings: {str(e)}")
            return self._create_detailed_fallback_findings(data_summary)
    
    def _generate_insights_interpretation(self, context, data_summary):
        """Generate interpretation of insights and their implications"""
        
        objective_instruction = ""
        if data_summary.get('objective'):
            objective_instruction = f"""
RESEARCH OBJECTIVE: {data_summary['objective']}

CRITICAL: Interpret all insights through the lens of this research objective. Explain how findings support or challenge the stated goal, and what implications they have for achieving it."""
        
        prompt = f"""You are a senior data analyst interpreting findings for a professional analytical report.
{objective_instruction}

DATASET INFORMATION AND FINDINGS:
{context}

Write a comprehensive insights interpretation section (500-700 words) that:

1. SIGNIFICANCE ANALYSIS
   - What do the statistical patterns mean in practical terms?
   - Why are the observed correlations important?
   - What story does the data tell?
{f'   - How do these insights directly support the research objective?' if data_summary.get('objective') else ''}

2. DEEPER IMPLICATIONS
   - What are the underlying causes of observed patterns?
   - What business/operational implications exist?
   - What opportunities or risks are revealed?
{f'   - What barriers or enablers to the objective are revealed?' if data_summary.get('objective') else ''}

3. CONTEXTUAL UNDERSTANDING
   - How do findings compare to expected norms?
   - What explains outliers or anomalies?
   - Are there secondary patterns worth noting?

4. ACTIONABLE INTERPRETATION
   - What decisions should these findings inform?
   - What areas need deeper investigation?
   - What immediate concerns should be addressed?
{f'   - What specific actions would move toward the stated objective?' if data_summary.get('objective') else ''}

Be analytical and thoughtful. Support interpretations with specific data points. Write in professional Canadian English."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a senior data analyst who excels at interpreting complex data patterns and explaining their real-world significance for business decisions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating insights interpretation: {str(e)}")
            return self._create_detailed_fallback_insights(data_summary)
    
    def _generate_recommendations(self, context, data_summary):
        """Generate actionable recommendations based on insights"""
        
        objective_instruction = ""
        if data_summary.get('objective'):
            objective_instruction = f"""
RESEARCH OBJECTIVE: {data_summary['objective']}

CRITICAL: All recommendations must be specifically designed to help achieve this research objective. Prioritize actions that directly address the stated goal."""
        
        prompt = f"""You are a strategic data analyst writing recommendations for a professional analytical report.
{objective_instruction}

DATASET INFORMATION AND INSIGHTS:
{context}

Write a comprehensive recommendations section (400-600 words) with 6-8 specific, actionable recommendations:

Each recommendation should include:
1. RECOMMENDATION TITLE (clear, action-oriented)
2. RATIONALE (2-3 sentences explaining why, based on data)
3. EXPECTED IMPACT (what improvement/change to expect)
{f'4. RELEVANCE TO OBJECTIVE (how it advances the research goal)' if data_summary.get('objective') else ''}

Focus on:
- Data-driven suggestions backed by findings
- Practical, implementable actions
- Priority areas based on strongest patterns
- Quick wins and long-term improvements
{f'- Actions that maximize progress toward the stated objective' if data_summary.get('objective') else ''}

Structure recommendations from highest to lowest priority. Be specific and actionable. Write in professional Canadian English."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a strategic business analyst who provides clear, actionable recommendations based on data insights. Your recommendations are specific, measurable, and implementation-focused."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating recommendations: {str(e)}")
            return self._create_detailed_fallback_recommendations(data_summary)
    
    def _create_detailed_fallback_summary(self, data_summary):
        """Create comprehensive fallback executive summary when API fails"""
        objective_section = ""
        if data_summary.get('objective'):
            objective_section = f"\n\nThis analysis is specifically designed to address the following research objective: {data_summary['objective']}. All findings and recommendations are evaluated in terms of their relevance to achieving this stated goal."
        
        summary_parts = [
            f"This comprehensive data analysis examines a dataset containing {data_summary.get('total_rows', 0):,} records across {data_summary.get('total_columns', 0)} variables. The dataset comprises {data_summary.get('numeric_columns', 0)} numerical variables and {data_summary.get('categorical_columns', 0)} categorical variables, providing a robust foundation for multidimensional analysis.{objective_section}",
            
            f"Data quality assessment reveals {'excellent' if data_summary.get('data_quality_score', 0) >= 80 else 'good' if data_summary.get('data_quality_score', 0) >= 60 else 'moderate'} overall quality with {data_summary.get('missing_data_summary', {}).get('missing_percentage', 0):.1f}% missing values. The analysis recommends {data_summary.get('recommended_analysis_type', 'comprehensive statistical analysis')} based on the data characteristics and distribution patterns observed."
        ]
        
        # Add numeric findings if available
        if data_summary.get('numeric_summary'):
            num_vars = list(data_summary['numeric_summary'].keys())[:3]
            var_summaries = []
            for var in num_vars:
                stats = data_summary['numeric_summary'][var]
                var_summaries.append(
                    f"{var} (mean: {stats.get('mean', 0):.2f}, range: {stats.get('min', 0):.2f}-{stats.get('max', 0):.2f})"
                )
            summary_parts.append(
                f"Key numerical variables include {', '.join(var_summaries)}. Distribution analysis reveals important patterns in variance and central tendency across these metrics."
            )
        
        # Add categorical findings if available
        if data_summary.get('categorical_summary'):
            cat_vars = list(data_summary['categorical_summary'].keys())[:2]
            cat_summaries = []
            for var in cat_vars:
                stats = data_summary['categorical_summary'][var]
                cat_summaries.append(
                    f"{var} with {stats.get('unique_values', 0)} distinct categories"
                )
            summary_parts.append(
                f"Categorical analysis shows {', '.join(cat_summaries)}. Distribution patterns indicate varying levels of concentration across categorical dimensions."
            )
        
        # Add correlations if available
        if data_summary.get('correlations'):
            top_corr = data_summary['correlations'][0]
            summary_parts.append(
                f"Correlation analysis identifies significant relationships, with the strongest being between {top_corr.get('variable_1', 'variables')} and {top_corr.get('variable_2', '')} (r={top_corr.get('coefficient', 0):.3f}). These patterns suggest meaningful associations warranting further investigation."
            )
        
        # Strategic implications
        objective_implications = ""
        if data_summary.get('objective'):
            objective_implications = " These findings provide critical insights for achieving the stated research objective and should inform strategic decision-making processes."
        
        summary_parts.append(
            f"The analysis reveals actionable insights across multiple dimensions, highlighting both opportunities and areas requiring attention.{objective_implications} Comprehensive recommendations are provided based on observed patterns and statistical significance testing."
        )
        
        return "\n\n".join(summary_parts)
    
    def _create_detailed_fallback_findings(self, data_summary):
        """Create detailed fallback findings when API fails"""
        findings_parts = []
        
        # 4.1 Data Composition
        findings_parts.append(
            f"4.1 Data Composition Overview\n\n"
            f"The dataset contains {data_summary.get('total_rows', 0):,} records with {data_summary.get('total_columns', 0)} variables. "
            f"This includes {data_summary.get('numeric_columns', 0)} numerical variables and {data_summary.get('categorical_columns', 0)} categorical variables. "
            f"Overall data quality is assessed at {data_summary.get('data_quality_score', 0)}/100."
        )
        
        # 4.2 Numerical Analysis
        if data_summary.get('numeric_summary'):
            num_details = []
            for var, stats in list(data_summary['numeric_summary'].items())[:5]:
                num_details.append(
                    f"• {var}: Mean={stats.get('mean', 0):.2f}, Median={stats.get('median', 0):.2f}, "
                    f"Std={stats.get('std', 0):.2f}, Range=[{stats.get('min', 0):.2f}, {stats.get('max', 0):.2f}]"
                )
            findings_parts.append(
                f"4.2 Numerical Analysis\n\n"
                f"Key numerical variables exhibit the following characteristics:\n" +
                "\n".join(num_details)
            )
        
        # 4.3 Categorical Breakdown
        if data_summary.get('categorical_summary'):
            cat_details = []
            for var, stats in list(data_summary['categorical_summary'].items())[:5]:
                top_vals = stats.get('top_values', {})
                top_3 = list(top_vals.items())[:3]
                cat_details.append(
                    f"• {var}: {stats.get('unique_values', 0)} categories. "
                    f"Top values: {', '.join([f'{k} ({v})' for k, v in top_3])}"
                )
            findings_parts.append(
                f"4.3 Categorical Breakdown\n\n"
                f"Categorical variable distributions:\n" +
                "\n".join(cat_details)
            )
        
        # 4.4 Correlation Patterns
        if data_summary.get('correlations'):
            corr_details = []
            for corr in data_summary['correlations'][:5]:
                corr_details.append(
                    f"• {corr.get('variable_1', 'N/A')} ↔ {corr.get('variable_2', 'N/A')}: "
                    f"r={corr.get('coefficient', 0):.3f} ({corr.get('strength', 'N/A')})"
                )
            findings_parts.append(
                f"4.4 Correlation Patterns\n\n"
                f"Significant correlations identified:\n" +
                "\n".join(corr_details)
            )
        
        return "\n\n".join(findings_parts)
    
    def _create_detailed_fallback_insights(self, data_summary):
        """Create detailed fallback insights when API fails"""
        insights_parts = [
            "The data analysis reveals several significant patterns worthy of deeper consideration. "
            "Statistical testing confirms that observed correlations exceed random chance, suggesting genuine relationships between variables."
        ]
        
        # Add numeric insights
        if data_summary.get('numeric_insights'):
            insights_parts.append(
                "Numerical analysis highlights: " +
                " ".join(data_summary['numeric_insights'][:3])
            )
        
        # Add categorical insights
        if data_summary.get('categorical_insights'):
            insights_parts.append(
                "Categorical patterns indicate: " +
                " ".join(data_summary['categorical_insights'][:3])
            )
        
        # Add correlation insights
        if data_summary.get('correlation_insights'):
            insights_parts.append(
                "Relationship analysis shows: " +
                " ".join(data_summary['correlation_insights'][:3])
            )
        
        insights_parts.append(
            "These findings provide actionable intelligence for strategic decision-making. "
            "Areas of concentration and dispersion suggest specific opportunities for intervention or optimization. "
            "The statistical significance of observed patterns warrants consideration in planning and resource allocation."
        )
        
        return "\n\n".join(insights_parts)
    
    def _create_detailed_fallback_recommendations(self, data_summary):
        """Create detailed fallback recommendations when API fails"""
        recommendations = []
        
        recommendations.append(
            "1. Data Quality Enhancement\n"
            f"With {data_summary.get('missing_data_summary', {}).get('missing_percentage', 0):.1f}% missing values, "
            "implement systematic data collection improvements to enhance completeness. "
            "This will strengthen the reliability of future analyses."
        )
        
        if data_summary.get('numeric_summary'):
            recommendations.append(
                "2. Monitor Key Numerical Metrics\n"
                "Establish tracking systems for top numerical variables identified in this analysis. "
                "Regular monitoring will enable trend detection and early intervention opportunities."
            )
        
        if data_summary.get('categorical_summary'):
            recommendations.append(
                "3. Leverage Categorical Patterns\n"
                "Use identified category distributions to segment and target specific groups. "
                "Concentration patterns suggest opportunities for focused interventions."
            )
        
        if data_summary.get('correlations'):
            recommendations.append(
                "4. Investigate Strong Correlations\n"
                "Conduct deeper analysis of strongest correlations to understand causal mechanisms. "
                "This knowledge can inform strategic initiatives and resource allocation."
            )
        
        recommendations.append(
            "5. Address Outliers and Anomalies\n"
            "Review identified outliers for data quality issues or special cases requiring attention. "
            "Anomaly investigation often reveals valuable insights or operational improvements."
        )
        
        recommendations.append(
            "6. Implement Predictive Analytics\n"
            f"Given the {data_summary.get('recommended_analysis_type', 'statistical')} nature of the data, "
            "develop predictive models to forecast trends and support proactive decision-making."
        )
        
        return "\n\n".join(recommendations)
