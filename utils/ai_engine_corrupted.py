import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AIEngine:
      def _generate_executive_summary(self, context, data_summary):
        """Generate comprehensive executive summary"""
        
        objective_context = ""
        if data_summary.get('objective'):
            objective_context = f"""
RESEARCH OBJECTIVE:
{data_summary['objective']}

IMPORTANT: Focus your analysis on addressing this specific research objective. All findings, patterns, and insights should be evaluated in terms of their relevance to achieving this stated objective.
"""
        
        prompt = f"""You are a data analyst writing an executive summary for a professional analytical report.

{objective_context}
DATASET INFORMATION:
{context}

Write a comprehensive executive summary (4-6 paragraphs, 400-500 words) that includes:owered comprehensive narrative generation using OpenAI GPT"""
    
    def __init__(self, config):
        """Initialize OpenAI client with configuration"""
        self.config = config
        self.model = config.get('model', 'gpt-4-turbo')
        self.temperature = config.get('temperature', 0.3)
        self.max_tokens = config.get('max_tokens', 4000)  # Increased for longer narratives
        
        # Initialize OpenAI client
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
    
    def generate_insights(self, data_summary, charts=None):
        """Generate comprehensive narrative insights from data summary"""
        
        # Build detailed context for AI
        context = self._build_comprehensive_context(data_summary)
        
        # Generate executive summary (3-5 paragraphs)
        executive_summary = self._generate_executive_summary(context, data_summary)
        
        # Generate detailed key findings (multi-section analysis)
        key_findings = self._generate_key_findings(context, data_summary)
        
        # Generate actionable recommendations
        recommendations = self._generate_recommendations(context, data_summary)
        
        # Generate insights and interpretation
        insights_interpretation = self._generate_insights_interpretation(context, data_summary)
        
        return {
            'executive_summary': executive_summary,
            'key_findings': key_findings,
            'recommendations': recommendations,
            'insights_interpretation': insights_interpretation
        }
    
    def _build_comprehensive_context(self, data_summary):
        """Build detailed context string from data summary with all insights"""
        context_parts = []
        
        # Research Objective (if provided)
        if data_summary.get('objective'):
            context_parts.append(f"=== RESEARCH OBJECTIVE ===")
            context_parts.append(data_summary['objective'])
            context_parts.append("")
        
        # Dataset Overview
        context_parts.append(f"=== DATASET OVERVIEW ===")
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
            context_parts.append(f"\n=== TOP CORRELATIONS ===")
            for corr in data_summary['correlations'][:8]:
                strength = corr.get('strength', '')
                context_parts.append(
                    f"{corr['var1']} ↔ {corr['var2']}: {corr['correlation']:.3f} ({strength})"
                )
        
        # Automated Insights
        if data_summary.get('numeric_insights'):
            context_parts.append(f"\n=== NUMERIC INSIGHTS ===")
            for insight in data_summary['numeric_insights'][:5]:
                context_parts.append(f"• {insight}")
        
        if data_summary.get('categorical_insights'):
            context_parts.append(f"\n=== CATEGORICAL INSIGHTS ===")
            for insight in data_summary['categorical_insights'][:5]:
                context_parts.append(f"• {insight}")
        
        if data_summary.get('correlation_insights'):
            context_parts.append(f"\n=== CORRELATION INSIGHTS ===")
            for insight in data_summary['correlation_insights'][:5]:
                context_parts.append(f"• {insight}")
        
        return "\n".join(context_parts)
    
    def _generate_executive_summary(self, context, data_summary):
        """Generate comprehensive executive summary"""
        
        objective_context = ""
        if data_summary.get('objective'):
            objective_context = f"""
RESEARCH OBJECTIVE:
{data_summary['objective']}

IMPORTANT: Focus your analysis on addressing this specific research objective. All findings, patterns, and insights should be evaluated in terms of their relevance to achieving this stated objective.
"""
        
        prompt = f"""You are a data analyst writing an executive summary for a professional analytical report.

{objective_context}
DATASET INFORMATION:
{context}

Write a comprehensive executive summary (4-6 paragraphs, 400-500 words) that includes:

PARAGRAPH 1: Overview
- Dataset size, scope, and purpose
- Primary variables and data types
{f'- How the dataset relates to the research objective' if data_summary.get('objective') else ''}

PARAGRAPH 2: Key Metrics
- Most important numerical findings (means, medians, ranges)
- Standout percentages or rates
{f'- Metrics most relevant to the stated objective' if data_summary.get('objective') else ''}

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
- Outliers or anomalies

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
            # Enhanced fallback with actual data
            return self._create_detailed_fallback_summary(data_summary)
    
    def _generate_key_findings(self, context, data_summary):
        """Generate detailed key findings with multiple subsections"""
        
        objective_context = ""
        if data_summary.get('objective'):
            objective_context = f"""
RESEARCH OBJECTIVE:
{data_summary['objective']}

IMPORTANT: Frame all findings in relation to this research objective. Highlight data patterns that directly inform or impact the stated objective.
"""
        
        prompt = f"""You are a data analyst writing the Key Findings section for a professional analytical report.

{objective_context}
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

4.5 Notable Patterns
- Any clusters or groupings
- Trends across variables
- Unexpected findings

Use specific numbers, create comparison tables where appropriate, and provide clear interpretations. Write in professional Canadian English with bullet points and structured formatting."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional data analyst writing detailed findings sections for analytical reports. You use specific statistics, percentages, and clear interpretations."},
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
        """Generate insights and interpretation section"""
        
        prompt = f"""You are a data analyst writing the Insights and Interpretation section of a professional report.

DATASET INFORMATION:
{context}

Write a comprehensive Insights and Interpretation section (500-700 words) that:

1. PATTERN ANALYSIS
   - What the statistical patterns reveal
   - Business or operational implications
   - Cause-and-effect relationships

2. COMPARATIVE ANALYSIS
   - How variables relate to each other
   - Segments or groups identified
   - Performance variations

3. ANOMALY INTERPRETATION
   - Explanation of outliers
   - Unusual distributions
   - Data quality considerations

4. CONTEXTUAL INSIGHTS
   - What the numbers mean in practice
   - Real-world implications
   - Areas of concern or opportunity

5. STRATEGIC CONSIDERATIONS
   - Long-term trends suggested
   - Risk factors identified
   - Opportunities highlighted

Use specific examples from the data. Provide clear, actionable interpretations. Write in professional Canadian English."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional data analyst providing insights and interpretations for business reports. You connect statistical findings to real-world implications."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return self._create_detailed_fallback_insights(data_summary)
    
    def _generate_recommendations(self, context, data_summary):
        """Generate actionable recommendations"""
        
        prompt = f"""You are a data analyst writing the Recommendations section for a strategic report.

DATASET INFORMATION:
{context}

Write a comprehensive Recommendations section (400-600 words) with 6-8 specific, actionable recommendations:

Format each recommendation as:

RECOMMENDATION #: [Clear Action Statement]
Rationale: [Why this is needed based on the data]
Expected Outcome: [What this will achieve]
Priority: [High/Medium/Low]

Focus on:
- Data-driven actions based on actual findings
- Specific, measurable recommendations
- Both quick wins and long-term strategies
- Risk mitigation and opportunity capture
- Process improvements and further analysis needs

Make recommendations realistic, actionable, and tied directly to insights from the data. Use professional Canadian English."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional data analyst providing strategic recommendations based on data analysis. You make specific, actionable suggestions tied to data insights."},
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
        """Create detailed fallback executive summary with actual data"""
        summary_parts = []
        
        # Paragraph 1: Overview
        summary_parts.append(
            f"This report presents a comprehensive analytical overview of a dataset comprising "
            f"{data_summary.get('total_rows', 0):,} records across {data_summary.get('total_columns', 0)} variables. "
            f"The dataset contains {data_summary.get('numeric_columns', 0)} numerical variables and "
            f"{data_summary.get('categorical_columns', 0)} categorical variables, providing a rich foundation "
            f"for multidimensional analysis."
        )
        
        # Paragraph 2: Key Metrics
        if data_summary.get('numeric_summary'):
            top_vars = list(data_summary['numeric_summary'].items())[:3]
            metrics = []
            for var, stats in top_vars:
                metrics.append(f"{var} (mean: {stats['mean']:.2f}, range: {stats['min']:.2f}-{stats['max']:.2f})")
            summary_parts.append(
                f"\n\nKey numerical metrics include: {'; '.join(metrics)}. "
                f"These variables exhibit varying degrees of dispersion and central tendency, "
                f"providing insights into the dataset's quantitative characteristics."
            )
        
        # Paragraph 3: Quality & Analysis
        quality_score = data_summary.get('data_quality_score', 0)
        summary_parts.append(
            f"\n\nThe dataset demonstrates a data quality score of {quality_score:.1f}/100, indicating "
            f"{'excellent' if quality_score >= 90 else 'good' if quality_score >= 75 else 'acceptable'} data integrity. "
            f"The recommended analytical approach is {data_summary.get('recommended_analysis_type', 'Exploratory Data Analysis')}, "
            f"which aligns with the dataset's structure and complexity."
        )
        
        # Paragraph 4: Patterns
        if data_summary.get('correlations'):
            top_corr = data_summary['correlations'][0]
            summary_parts.append(
                f"\n\nAnalysis reveals significant correlations within the data, most notably between "
                f"{top_corr['var1']} and {top_corr['var2']} (r={top_corr['correlation']:.3f}), "
                f"suggesting meaningful relationships that warrant further investigation for strategic insights."
            )
        
        return "".join(summary_parts)
    
    def _create_detailed_fallback_findings(self, data_summary):
        """Create detailed fallback findings with structure"""
        findings = []
        
        findings.append("4.1 DATA COMPOSITION OVERVIEW\n")
        findings.append(f"Total Records: {data_summary.get('total_rows', 0):,}")
        findings.append(f"Total Variables: {data_summary.get('total_columns', 0)}")
        findings.append(f"Numeric Variables: {data_summary.get('numeric_columns', 0)}")
        findings.append(f"Categorical Variables: {data_summary.get('categorical_columns', 0)}\n")
        
        if data_summary.get('numeric_summary'):
            findings.append("\n4.2 NUMERICAL ANALYSIS\n")
            for col, stats in list(data_summary['numeric_summary'].items())[:5]:
                findings.append(f"\n{col}:")
                findings.append(f"  - Mean: {stats['mean']:.2f}")
                findings.append(f"  - Median: {stats['median']:.2f}")
                findings.append(f"  - Std Dev: {stats['std']:.2f}")
                findings.append(f"  - Range: [{stats['min']:.2f}, {stats['max']:.2f}]")
        
        if data_summary.get('categorical_summary'):
            findings.append("\n\n4.3 CATEGORICAL BREAKDOWN\n")
            for col, stats in list(data_summary['categorical_summary'].items())[:5]:
                findings.append(f"\n{col}: {stats['unique_values']} unique values")
                top_val = list(stats.get('top_values', {}).items())[0] if stats.get('top_values') else ('N/A', 0)
                findings.append(f"  - Top category: {top_val[0]} ({top_val[1]} occurrences)")
        
        if data_summary.get('correlations'):
            findings.append("\n\n4.4 CORRELATION PATTERNS\n")
            for corr in data_summary['correlations'][:5]:
                findings.append(f"  - {corr['var1']} ↔ {corr['var2']}: {corr['correlation']:.3f}")
        
        return "\n".join(findings)
    
    def _create_detailed_fallback_insights(self, data_summary):
        """Create detailed fallback insights"""
        insights = []
        
        insights.append("PATTERN ANALYSIS")
        insights.append("The dataset exhibits structured patterns across multiple dimensions. ")
        insights.append("Numerical variables demonstrate varying degrees of dispersion, ")
        insights.append("while categorical variables show concentration in specific categories.\n")
        
        insights.append("\nCOMPARATIVE ANALYSIS")
        if data_summary.get('correlations'):
            top_corr = data_summary['correlations'][0]
            insights.append(f"Strong relationships exist between {top_corr['var1']} and {top_corr['var2']}, ")
            insights.append(f"with a correlation coefficient of {top_corr['correlation']:.3f}. ")
            insights.append("This suggests interdependencies that may influence strategic decisions.\n")
        
        insights.append("\nSTRATEGIC CONSIDERATIONS")
        insights.append("The analysis reveals opportunities for optimization and areas requiring attention. ")
        insights.append("Data quality is generally strong, supporting reliable decision-making. ")
        insights.append("Further segmentation analysis may yield additional actionable insights.")
        
        return "".join(insights)
    
    def _create_detailed_fallback_recommendations(self, data_summary):
        """Create detailed fallback recommendations"""
        recs = []
        
        recs.append("Based on the comprehensive data analysis, the following recommendations are proposed:\n")
        
        recs.append("\n1. CONDUCT DEEP-DIVE SEGMENTATION ANALYSIS")
        recs.append("   Rationale: Multiple variables show potential for segmentation")
        recs.append("   Expected Outcome: Identification of distinct patterns and actionable sub-groups\n")
        
        recs.append("\n2. MONITOR KEY CORRELATIONS")
        if data_summary.get('correlations'):
            top_corr = data_summary['correlations'][0]
            recs.append(f"   Focus: {top_corr['var1']} and {top_corr['var2']} relationship")
        recs.append("   Expected Outcome: Better predictive capability\n")
        
        recs.append("\n3. ENHANCE DATA COLLECTION FOR LOW-QUALITY AREAS")
        if data_summary.get('missing_data_summary'):
            recs.append(f"   Current missing data: {data_summary['missing_data_summary'].get('missing_percentage', 0):.2f}%")
        recs.append("   Expected Outcome: Improved data completeness and analysis reliability\n")
        
        recs.append("\n4. IMPLEMENT REGULAR MONITORING")
        recs.append("   Rationale: Track changes over time")
        recs.append("   Expected Outcome: Early detection of trends and anomalies\n")
        
        recs.append("\n5. DEVELOP PREDICTIVE MODELS")
        recs.append("   Rationale: Leverage strong correlations identified")
        recs.append("   Expected Outcome: Enhanced forecasting capabilities")
        
        return "".join(recs)
