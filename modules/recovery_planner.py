# # # modules/recovery_planner.py

# # class RecoveryPlanner:
# #     """Generates personalized recovery plans based on player stats"""
    
# #     def __init__(self):
# #         print(" Initializing Recovery Planner...")
    
# #     def generate_recovery_plan(self, player_stats, injury_prediction):
# #         """
# #         Creates comprehensive recovery plan
        
# #         Args:
# #             player_stats: Player statistics from analyzer
# #             injury_prediction: Output from InjuryPredictor
        
# #         Returns:
# #             Dictionary with complete recovery plan
# #         """
# #         # Calculate fatigue score (0-500)
# #         fatigue_score = self._calculate_fatigue_score(player_stats)
        
# #         # Generate plan
# #         plan = {
# #             'player_id': player_stats.get('player_id', 'Unknown'),
# #             'match_date': player_stats.get('match_date', 'Recent Match'),
            
# #             # Fatigue assessment
# #             'fatigue_level': self._get_fatigue_level(fatigue_score),
# #             'fatigue_score': int(fatigue_score),
# #             'fatigue_max': 500,
            
# #             # Key metrics from match
# #             'key_metrics': self._extract_key_metrics(player_stats),
            
# #             # Position insights
# #             'position': player_stats.get('position', 'Unknown'),
# #             'position_insights': self._get_position_insights(player_stats),
            
# #             # Recovery prescription
# #             'recovery_prescription': self._generate_prescription(fatigue_score, injury_prediction, player_stats),
            
# #             # Warnings
# #             'warnings': self._generate_warnings(injury_prediction, player_stats),
            
# #             # Recovery timeline
# #             'timeline': self._generate_recovery_timeline(fatigue_score, injury_prediction),
            
# #             # Diet suggestions (for wellness team)
# #             'diet_suggestions': self._generate_diet_suggestions(fatigue_score, player_stats)
# #         }
        
# #         return plan
    
# #     def _calculate_fatigue_score(self, stats):
# #         """Calculate fatigue score from 0-500 based on match intensity"""
# #         score = 0
        
# #         # Sprints are highly fatiguing
# #         score += stats.get('sprint_count', 0) * 3
        
# #         # Distance contributes to cumulative fatigue
# #         score += stats.get('total_distance_km', 0) * 15
        
# #         # Accelerations cause muscle micro-tears
# #         score += stats.get('accelerations', 0) * 0.8
        
# #         # Decelerations are even more damaging (eccentric loading)
# #         score += stats.get('decelerations', 0) * 1.2
        
# #         # High speed increases muscle strain
# #         score += stats.get('max_speed', 0) * 2
        
# #         # High intensity running
# #         score += stats.get('high_intensity_distance_km', 0) * 20
        
# #         # Cap at 500
# #         return min(score, 500)
    
# #     def _get_fatigue_level(self, score):
# #         """Convert fatigue score to human-readable level"""
# #         if score >= 400:
# #             return "CRITICAL 🔥🔥🔥"
# #         elif score >= 300:
# #             return "HIGH 🔥🔥"
# #         elif score >= 200:
# #             return "MODERATE 🔥"
# #         elif score >= 100:
# #             return "MILD ⚠️"
# #         else:
# #             return "LOW ✅"
    
# #     def _extract_key_metrics(self, stats):
# #         """Extract and format key metrics for display"""
# #         metrics = []
        
# #         if stats.get('sprint_count', 0) > 0:
# #             metrics.append(f"{stats['sprint_count']} explosive sprints")
        
# #         if stats.get('total_distance_km', 0) > 0:
# #             metrics.append(f"{stats['total_distance_km']:.1f}km total distance")
        
# #         if stats.get('accelerations', 0) > 0:
# #             metrics.append(f"{stats['accelerations']} rapid accelerations")
        
# #         if stats.get('decelerations', 0) > 0:
# #             metrics.append(f"{stats['decelerations']} hard decelerations")
        
# #         if stats.get('max_speed', 0) > 0:
# #             metrics.append(f"{stats['max_speed']:.1f} km/h top speed")
        
# #         return metrics
    
# #     def _get_position_insights(self, stats):
# #         """Generate position-specific insights"""
# #         position = stats.get('position', '').lower()
# #         insights = []
        
# #         if 'goalkeeper' in position:
# #             insights.append("High-intensity reactions and jumps")
# #             insights.append("Focus on shoulder and core recovery")
            
# #         elif 'defender' in position:
# #             insights.append("Significant physical duels and tackles")
# #             insights.append("Focus on hamstring and knee recovery")
            
# #         elif 'midfielder' in position:
# #             insights.append("High cardiovascular load detected")
# #             insights.append("Significant lateral movement and turns")
            
# #         elif 'forward' in position or 'attacking' in position:
# #             insights.append("Explosive sprint repetitions")
# #             insights.append("Focus on quadriceps and calf recovery")
            
# #         else:
# #             insights.append("General high-intensity match detected")
# #             insights.append("Full-body recovery recommended")
        
# #         return insights
    
# #     def _generate_prescription(self, fatigue_score, injury_prediction, stats):
# #         """Generate recovery prescription"""
        
# #         # Determine rest days based on fatigue
# #         if fatigue_score >= 400:
# #             rest_days = 3
# #             hydration = "Drink extra 2.5L water today"
# #             sleep = "Aim for 9+ hours for next 3 nights"
            
# #         elif fatigue_score >= 300:
# #             rest_days = 2
# #             hydration = "Drink extra 2.0L water today"
# #             sleep = "Aim for 9+ hours tonight"
            
# #         elif fatigue_score >= 200:
# #             rest_days = 1
# #             hydration = "Drink extra 1.5L water today"
# #             sleep = "Aim for 8+ hours tonight"
            
# #         else:
# #             rest_days = 0  # Active recovery
# #             hydration = "Maintain normal hydration"
# #             sleep = "7-8 hours recommended"
        
# #         # Activities based on fatigue and position
# #         activities = []
# #         position = stats.get('position', '').lower()
        
# #         if fatigue_score >= 300:
# #             activities.append(f"{rest_days} days complete rest")
# #             activities.append("Ice bath (10-15 minutes)")
# #             if 'midfielder' in position or 'forward' in position:
# #                 activities.append("Leg compression sleeves")
        
# #         elif fatigue_score >= 200:
# #             activities.append("24 hours complete rest")
# #             activities.append("Foam rolling (full body)")
# #             activities.append("Light stretching routine")
        
# #         else:
# #             activities.append("Active recovery day")
# #             activities.append("Light jogging or swimming")
# #             activities.append("Dynamic stretching")
        
# #         # Add cryotherapy for high fatigue
# #         if fatigue_score >= 350:
# #             activities.append("Consider cryotherapy session")
        
# #         # Nutrition suggestions
# #         nutrition = []
# #         if fatigue_score >= 250:
# #             nutrition.append("High-carb meal within 2 hours post-match")
# #             nutrition.append("Increase protein intake by 20-30g/day")
# #         else:
# #             nutrition.append("Balanced post-match meal")
# #             nutrition.append("Normal protein intake")
        
# #         if injury_prediction['risk_score'] > 0.6:
# #             nutrition.append("Anti-inflammatory foods (berries, turmeric)")
        
# #         return {
# #             'rest_days': rest_days,
# #             'hydration': hydration,
# #             'sleep': sleep,
# #             'activities': activities,
# #             'nutrition': nutrition
# #         }
    
# #     def _generate_warnings(self, injury_prediction, stats):
# #         """Generate warnings based on injury risk and stats"""
# #         warnings = []
        
# #         # High injury risk warnings
# #         if injury_prediction['risk_score'] > 0.7:
# #             warnings.append(f"CRITICAL injury risk ({injury_prediction['risk_score']*100:.0f}%) - Consider medical consultation")
        
# #         elif injury_prediction['risk_score'] > 0.5:
# #             warnings.append(f"HIGH injury risk ({injury_prediction['risk_score']*100:.0f}%) - Extra caution needed")
        
# #         # Specific injury warnings
# #         for injury in injury_prediction.get('likely_injuries', []):
# #             if injury['probability'] > 0.6:
# #                 warnings.append(f"High risk of {injury['type']} - {', '.join(injury['reasons'])}")
        
# #         # Fatigue warnings
# #         fatigue_score = self._calculate_fatigue_score(stats)
# #         if fatigue_score > 350:
# #             warnings.append("Extreme fatigue detected - Minimum 72h before next intense match")
# #         elif fatigue_score > 250:
# #             warnings.append("High fatigue - Allow 48h minimum recovery before next match")
        
# #         # Position-specific warnings
# #         position = stats.get('position', '').lower()
# #         if 'goalkeeper' in position and stats.get('max_speed', 0) < 20:
# #             warnings.append("Low max speed detected - Check for any mobility issues")
        
# #         if stats.get('sprint_count', 0) > 40:
# #             warnings.append("Very high sprint count - Monitor hamstring tightness")
        
# #         return warnings
    
# #     def _generate_recovery_timeline(self, fatigue_score, injury_prediction):
# #         """Generate day-by-day recovery timeline"""
# #         timeline = []
        
# #         if fatigue_score >= 400:
# #             timeline = [
# #                 "Day 0: Complete rest + ice bath + compression",
# #                 "Day 1: Complete rest + hydration focus",
# #                 "Day 2: Light walking (15-20 mins) + stretching",
# #                 "Day 3: 30% training intensity + foam rolling",
# #                 "Day 4: 50% training intensity",
# #                 "Day 5: 75% training intensity",
# #                 "Day 6: Full clearance expected"
# #             ]
        
# #         elif fatigue_score >= 300:
# #             timeline = [
# #                 "Day 0: Complete rest + hydration",
# #                 "Day 1: Ice bath + light stretching",
# #                 "Day 2: Light walk (20-30 mins) + foam rolling",
# #                 "Day 3: 50% training intensity",
# #                 "Day 4: 75% training intensity",
# #                 "Day 5: Full clearance expected"
# #             ]
        
# #         elif fatigue_score >= 200:
# #             timeline = [
# #                 "Day 0: Active recovery + hydration",
# #                 "Day 1: Light jogging (20 mins) + stretching",
# #                 "Day 2: 70% training intensity",
# #                 "Day 3: Full clearance expected"
# #             ]
        
# #         else:
# #             timeline = [
# #                 "Day 0: Normal recovery + hydration",
# #                 "Day 1: Return to full training"
# #             ]
        
# #         # Add injury-specific adjustments
# #         if injury_prediction['risk_score'] > 0.7:
# #             timeline.insert(0, " Medical consultation recommended before returning")
        
# #         return timeline
    
# #     def _generate_diet_suggestions(self, fatigue_score, stats):
# #         """Generate diet suggestions for wellness team"""
# #         suggestions = {
# #             'general': [],
# #             'macronutrients': {},
# #             'timing': [],
# #             'supplements': []
# #         }
        
# #         if fatigue_score >= 300:
# #             suggestions['general'].append("High-calorie recovery diet needed")
# #             suggestions['macronutrients'] = {
# #                 'protein': "1.6-2.0g per kg body weight",
# #                 'carbs': "6-8g per kg body weight",
# #                 'hydration': "40-60ml per kg body weight"
# #             }
# #             suggestions['timing'].append("Carb-protein meal within 30min post-match")
# #             suggestions['timing'].append("Small meals every 3-4 hours")
# #             suggestions['supplements'].append("Consider: Whey protein, BCAAs, Electrolytes")
        
# #         elif fatigue_score >= 200:
# #             suggestions['general'].append("Moderate recovery diet")
# #             suggestions['macronutrients'] = {
# #                 'protein': "1.4-1.6g per kg body weight",
# #                 'carbs': "5-6g per kg body weight",
# #                 'hydration': "35-45ml per kg body weight"
# #             }
# #             suggestions['timing'].append("Recovery meal within 2 hours")
# #             suggestions['supplements'].append("Consider: Electrolytes, Vitamin C")
        
# #         else:
# #             suggestions['general'].append("Normal maintenance diet")
# #             suggestions['macronutrients'] = {
# #                 'protein': "1.2-1.4g per kg body weight",
# #                 'carbs': "3-5g per kg body weight",
# #                 'hydration': "30-35ml per kg body weight"
# #             }
        
# #         # Position-specific suggestions
# #         position = stats.get('position', '').lower()
# #         if 'midfielder' in position or 'forward' in position:
# #             suggestions['general'].append("Focus on carbohydrate loading pre-match")
        
# #         if stats.get('sprint_count', 0) > 30:
# #             suggestions['supplements'].append("Extra magnesium for muscle recovery")
        
# #         return suggestions
# # modules/recovery_planner.py

# class RecoveryPlanner:
#     """Generates comprehensive recovery plans based on training dataset patterns"""
    
#     def __init__(self):
#         print("💊 Initializing Recovery Planner...")
#         print("   Loaded recovery protocols for 28 injury types")
#         print("   Loaded 8-tier fatigue classification system")
    
#     def generate_recovery_plan(self, player_stats, injury_prediction):
#         """Creates comprehensive recovery plan"""
        
#         # Calculate fatigue score (0-500 scale from training)
#         fatigue_score = self._calculate_fatigue_score(player_stats)
        
#         # Generate comprehensive plan
#         plan = {
#             'player_id': player_stats.get('player_id', 'Unknown'),
#             'match_date': player_stats.get('match_date', 'Recent Match'),
            
#             # Fatigue assessment
#             'fatigue_level': self._get_fatigue_level_enhanced(fatigue_score),
#             'fatigue_score': int(fatigue_score),
#             'fatigue_max': 500,
            
#             # Key metrics
#             'key_metrics': self._extract_key_metrics(player_stats),
            
#             # Position insights
#             'position': player_stats.get('position', 'Unknown'),
#             'position_insights': self._get_position_insights_enhanced(player_stats),
            
#             # Recovery prescription
#             'recovery_prescription': self._generate_prescription_enhanced(fatigue_score, injury_prediction, player_stats),
            
#             # Warnings
#             'warnings': self._generate_warnings_enhanced(injury_prediction, player_stats),
            
#             # Recovery timeline
#             'timeline': self._generate_recovery_timeline_detailed(fatigue_score, injury_prediction),
            
#             # Diet suggestions
#             'diet_suggestions': self._generate_diet_suggestions_enhanced(fatigue_score, player_stats)
#         }
        
#         return plan
    
#     def _calculate_fatigue_score(self, stats):
#         """Calculate fatigue score (0-500) matching training dataset"""
#         score = 0
        
#         # Sprints (highly fatiguing)
#         score += stats.get('sprint_count', 0) * 3
        
#         # Distance (cumulative fatigue)
#         score += stats.get('total_distance_km', 0) * 15
        
#         # Accelerations (muscle micro-tears)
#         score += stats.get('accelerations', 0) * 0.8
        
#         # Decelerations (eccentric loading)
#         score += stats.get('decelerations', 0) * 1.2
        
#         # High speed (muscle strain)
#         score += stats.get('max_speed', 0) * 2
        
#         # High intensity running
#         score += stats.get('high_intensity_distance_km', 0) * 20
        
#         return min(score, 500)
    
#     def _get_fatigue_level_enhanced(self, score):
#         """8-level fatigue classification"""
#         if score >= 450:
#             return "CRITICAL 🔥🔥🔥"
#         elif score >= 400:
#             return "CRITICAL 🔥🔥🔥"
#         elif score >= 350:
#             return "VERY HIGH 🔥🔥"
#         elif score >= 300:
#             return "HIGH 🔥🔥"
#         elif score >= 250:
#             return "MODERATE-HIGH 🔥"
#         elif score >= 200:
#             return "MODERATE 🔥"
#         elif score >= 100:
#             return "MILD ⚠️"
#         else:
#             return "LOW ✅"
    
#     def _extract_key_metrics(self, stats):
#         """Extract key metrics for display"""
#         metrics = []
        
#         if stats.get('sprint_count', 0) > 0:
#             metrics.append(f"{stats['sprint_count']} explosive sprints")
        
#         if stats.get('total_distance_km', 0) > 0:
#             metrics.append(f"{stats['total_distance_km']:.1f}km total distance")
        
#         if stats.get('accelerations', 0) > 0:
#             metrics.append(f"{stats['accelerations']} rapid accelerations")
        
#         if stats.get('decelerations', 0) > 0:
#             metrics.append(f"{stats['decelerations']} hard decelerations")
        
#         if stats.get('max_speed', 0) > 0:
#             metrics.append(f"{stats['max_speed']:.1f} km/h top speed")
        
#         if stats.get('high_intensity_distance_km', 0) > 0:
#             metrics.append(f"{stats['high_intensity_distance_km']:.2f}km high-intensity")
        
#         return metrics
    
#     def _get_position_insights_enhanced(self, stats):
#         """Enhanced position-specific insights"""
#         position = stats.get('position', '').lower()
#         insights = []
        
#         if 'goalkeeper' in position:
#             insights.append("High-intensity reactions and explosive movements")
#             insights.append("Significant shoulder and core loading detected")
#             insights.append("Focus on upper body and rotational recovery")
            
#         elif 'defender' in position:
#             insights.append("High physical contact and dueling detected")
#             insights.append("Significant hamstring and knee stress")
#             insights.append("Lower body recovery priority")
            
#         elif 'midfielder' in position:
#             insights.append("Extreme cardiovascular demand detected")
#             insights.append("High-volume running with frequent direction changes")
#             insights.append("Full-body recovery with cardiovascular focus")
            
#         elif 'forward' in position or 'attacking' in position or 'striker' in position or 'winger' in position:
#             insights.append("High explosive sprint repetitions")
#             insights.append("Significant quadriceps and calf loading")
#             insights.append("Focus on lower leg and hamstring recovery")
            
#         else:
#             insights.append("High-intensity match performance detected")
#             insights.append("Full-body recovery recommended")
        
#         return insights
    
#     def _generate_prescription_enhanced(self, fatigue_score, injury_prediction, stats):
#         """Enhanced recovery prescription with detailed protocols"""
        
#         # Determine rest days based on 8-level fatigue
#         if fatigue_score >= 450:
#             rest_days = 5
#             hydration = "Drink extra 3.0L+ water today, 2.5L next 2 days"
#             sleep = "CRITICAL: 10+ hours for next 5 nights"
            
#         elif fatigue_score >= 400:
#             rest_days = 4
#             hydration = "Drink extra 2.8L water today, 2.3L next 2 days"
#             sleep = "Aim for 9.5+ hours for next 4 nights"
            
#         elif fatigue_score >= 350:
#             rest_days = 3
#             hydration = "Drink extra 2.5L water today"
#             sleep = "Aim for 9+ hours for next 3 nights"
            
#         elif fatigue_score >= 300:
#             rest_days = 3
#             hydration = "Drink extra 2.0L water today"
#             sleep = "Aim for 9+ hours for next 2 nights"
            
#         elif fatigue_score >= 250:
#             rest_days = 2
#             hydration = "Drink extra 1.8L water today"
#             sleep = "Aim for 8.5+ hours for next 2 nights"
            
#         elif fatigue_score >= 200:
#             rest_days = 2
#             hydration = "Drink extra 1.5L water today"
#             sleep = "Aim for 8+ hours tonight"
            
#         elif fatigue_score >= 100:
#             rest_days = 1
#             hydration = "Drink extra 1.0L water today"
#             sleep = "Aim for 8 hours tonight"
            
#         else:
#             rest_days = 0  # Active recovery
#             hydration = "Maintain normal hydration (3L)"
#             sleep = "7-8 hours recommended"
        
#         # Enhanced activities based on fatigue and injury risk
#         activities = []
#         position = stats.get('position', '').lower()
#         risk_score = injury_prediction.get('raw_risk_score', 0)
        
#         if fatigue_score >= 400 or risk_score >= 135:
#             activities.append(f"{rest_days} days complete rest - NO training")
#             activities.append("Ice bath (10-15 minutes) within 2 hours")
#             activities.append("Compression garments 24/7 for first 48h")
#             activities.append("Elevation exercises 3x daily")
#             activities.append("Professional massage therapy (day 2)")
#             if 'midfielder' in position or 'forward' in position:
#                 activities.append("Full leg compression sleeves")
#                 activities.append("Consider cryotherapy session")
        
#         elif fatigue_score >= 300:
#             activities.append(f"{rest_days} days complete rest")
#             activities.append("Ice bath (10-15 minutes)")
#             activities.append("Compression sleeves recommended")
#             activities.append("Foam rolling (full body, 20 mins)")
#             activities.append("Light stretching routine (15 mins)")
        
#         elif fatigue_score >= 200:
#             activities.append("24-48 hours complete rest")
#             activities.append("Ice bath or contrast therapy")
#             activities.append("Foam rolling (full body)")
#             activities.append("Dynamic stretching routine")
        
#         else:
#             activities.append("Active recovery day")
#             activities.append("Light jogging (20-30 mins) or swimming")
#             activities.append("Dynamic stretching")
#             activities.append("Mobility exercises")
        
#         # Nutrition suggestions (enhanced)
#         nutrition = []
#         if fatigue_score >= 350:
#             nutrition.append("CRITICAL: High-carb meal within 30 minutes post-match")
#             nutrition.append("Increase protein to 2.0g/kg body weight")
#             nutrition.append("Anti-inflammatory supplements (omega-3, turmeric)")
#             nutrition.append("Electrolyte drinks every 2 hours for 24h")
#         elif fatigue_score >= 250:
#             nutrition.append("High-carb meal within 1 hour post-match")
#             nutrition.append("Increase protein by 30g/day (1.6-1.8g/kg)")
#             nutrition.append("Anti-inflammatory foods (berries, fish)")
#         elif fatigue_score >= 150:
#             nutrition.append("Balanced post-match meal within 2 hours")
#             nutrition.append("Increase protein by 20g/day")
#         else:
#             nutrition.append("Normal balanced diet")
#             nutrition.append("Standard protein intake (1.2-1.4g/kg)")
        
#         # Injury-specific nutrition
#         if risk_score >= 110:
#             nutrition.append("Extra: Collagen peptides, Vitamin D, Magnesium")
        
#         return {
#             'rest_days': rest_days,
#             'hydration': hydration,
#             'sleep': sleep,
#             'activities': activities,
#             'nutrition': nutrition
#         }
    
#     def _generate_warnings_enhanced(self, injury_prediction, stats):
#         """Enhanced warnings with more detail"""
#         warnings = []
        
#         risk_score = injury_prediction.get('raw_risk_score', 0)
#         risk_level = injury_prediction.get('risk_level', '')
        
#         # Critical injury risk warnings
#         if risk_score >= 160:
#             warnings.append(f"CRITICAL injury risk (Level: {risk_level}) - IMMEDIATE medical assessment REQUIRED")
#             warnings.append("Do NOT train until cleared by medical staff")
#         elif risk_score >= 135:
#             warnings.append(f"CRITICAL injury risk ({risk_level}) - Medical consultation strongly advised")
#             warnings.append("Minimum 72h rest before any intense activity")
#         elif risk_score >= 110:
#             warnings.append(f"HIGH injury risk ({risk_level}) - Extra precautions needed")
#             warnings.append("48h minimum rest, monitor symptoms closely")
#         elif risk_score >= 90:
#             warnings.append(f"MODERATE-HIGH injury risk ({risk_level})")
#             warnings.append("24h rest minimum, careful progression")
        
#         # Specific injury warnings
#         for injury in injury_prediction.get('likely_injuries', [])[:3]:
#             if injury['probability'] > 0.7:
#                 warnings.append(f"Very high risk of {injury['type']} ({injury['probability']*100:.0f}%): {', '.join(injury['reasons'])}")
#             elif injury['probability'] > 0.5:
#                 warnings.append(f"High risk of {injury['type']}: {', '.join(injury['reasons'][:2])}")
        
#         # Fatigue warnings
#         fatigue_score = self._calculate_fatigue_score(stats)
#         if fatigue_score > 450:
#             warnings.append("EXTREME fatigue detected - Minimum 5 days before next match")
#         elif fatigue_score > 400:
#             warnings.append("Critical fatigue - Minimum 4 days recovery needed")
#         elif fatigue_score > 350:
#             warnings.append("Very high fatigue - 72h minimum before next intense match")
#         elif fatigue_score > 300:
#             warnings.append("High fatigue - Allow 48-72h recovery")
#         elif fatigue_score > 250:
#             warnings.append("Moderate-high fatigue - 48h minimum recovery")
        
#         # Position-specific warnings
#         position = stats.get('position', '').lower()
#         if stats.get('sprint_count', 0) > 40:
#             warnings.append("Extremely high sprint count - Monitor hamstring tightness closely")
        
#         if stats.get('total_distance_km', 0) > 13:
#             warnings.append("Excessive distance covered - Risk of overuse injuries")
        
#         if 'midfielder' in position and fatigue_score > 300:
#             warnings.append("High cardiovascular load - Heart rate monitoring recommended")
        
#         return warnings
    
#     def _generate_recovery_timeline_detailed(self, fatigue_score, injury_prediction):
#         """Detailed 7-day recovery timeline"""
#         timeline = []
#         risk_score = injury_prediction.get('raw_risk_score', 0)
        
#         if fatigue_score >= 450 or risk_score >= 160:
#             timeline = [
#                 "Day 0 (Today): Complete rest + ice bath + compression + elevation",
#                 "Day 1: Complete rest + hydration focus + professional massage",
#                 "Day 2: Complete rest + gentle passive stretching (10 mins)",
#                 "Day 3: Light walking (15-20 mins) + foam rolling",
#                 "Day 4: Light walking (20-30 mins) + dynamic stretching",
#                 "Day 5: 30% training intensity + monitor symptoms",
#                 "Day 6: 50% training intensity if pain-free",
#                 "Day 7: Medical clearance check before progression"
#             ]
#         elif fatigue_score >= 400 or risk_score >= 135:
#             timeline = [
#                 "Day 0: Complete rest + ice bath + compression",
#                 "Day 1: Complete rest + hydration + light stretching",
#                 "Day 2: Light walking (20 mins) + foam rolling",
#                 "Day 3: Light jog (20 mins, 60% intensity) + stretching",
#                 "Day 4: 50% training intensity",
#                 "Day 5: 70% training intensity",
#                 "Day 6: 85% training intensity",
#                 "Day 7: Full clearance expected (if symptom-free)"
#             ]
#         elif fatigue_score >= 350:
#             timeline = [
#                 "Day 0: Complete rest + ice bath",
#                 "Day 1: Light walking (25 mins) + foam rolling",
#                 "Day 2: Light jog (25 mins) + dynamic stretching",
#                 "Day 3: 60% training intensity",
#                 "Day 4: 80% training intensity",
#                 "Day 5: Full clearance expected"
#             ]
#         elif fatigue_score >= 300:
#             timeline = [
#                 "Day 0: Active recovery + hydration",
#                 "Day 1: Light jog (30 mins) + stretching",
#                 "Day 2: 70% training intensity",
#                 "Day 3: 90% training intensity",
#                 "Day 4: Full clearance expected"
#             ]
#         elif fatigue_score >= 200:
#             timeline = [
#                 "Day 0: Active recovery + hydration",
#                 "Day 1: Light jog (30 mins)",
#                 "Day 2: 80% training intensity",
#                 "Day 3: Full clearance expected"
#             ]
#         else:
#             timeline = [
#                 "Day 0: Normal recovery + hydration",
#                 "Day 1: Return to full training"
#             ]
        
#         # Add injury-specific adjustments
#         if risk_score >= 135:
#             timeline.insert(0, "⚕️ Medical consultation required before starting timeline")
        
#         return timeline
    
#     def _generate_diet_suggestions_enhanced(self, fatigue_score, stats):
#         """Enhanced diet suggestions"""
#         suggestions = {
#             'general': [],
#             'macronutrients': {},
#             'timing': [],
#             'supplements': [],
#             'sample_meals': []
#         }
        
#         if fatigue_score >= 400:
#             suggestions['general'].append("HIGH-CALORIE recovery diet essential")
#             suggestions['general'].append("Focus on nutrient timing for optimal recovery")
#             suggestions['macronutrients'] = {
#                 'protein': "2.0-2.2g per kg body weight",
#                 'carbs': "8-10g per kg body weight",
#                 'fats': "1.0-1.2g per kg body weight",
#                 'hydration': "50-60ml per kg body weight"
#             }
#             suggestions['timing'].append("Post-match meal within 30 minutes (carb+protein 4:1)")
#             suggestions['timing'].append("Protein-rich snack every 3 hours")
#             suggestions['timing'].append("Pre-sleep protein (casein) for muscle repair")
#             suggestions['supplements'].append("CRITICAL: Whey protein, BCAAs, Electrolytes")
#             suggestions['supplements'].append("Anti-inflammatory: Omega-3, Turmeric")
#             suggestions['supplements'].append("Recovery: Vitamin D, Magnesium, Zinc")
#             suggestions['sample_meals'].append("Post-match: Rice bowl with chicken, sweet potato")
#             suggestions['sample_meals'].append("2h later: Greek yogurt with berries and honey")
#             suggestions['sample_meals'].append("Dinner: Salmon, quinoa, vegetables")
        
#         elif fatigue_score >= 300:
#             suggestions['general'].append("High-calorie recovery diet recommended")
#             suggestions['macronutrients'] = {
#                 'protein': "1.6-2.0g per kg body weight",
#                 'carbs': "6-8g per kg body weight",
#                 'hydration': "40-50ml per kg body weight"
#             }
#             suggestions['timing'].append("Post-match meal within 1 hour")
#             suggestions['timing'].append("Small meals every 3-4 hours")
#             suggestions['supplements'].append("Whey protein, BCAAs, Electrolytes")
#             suggestions['supplements'].append("Consider: Omega-3, Vitamin C")
#             suggestions['sample_meals'].append("Post-match: Pasta with lean meat")
#             suggestions['sample_meals'].append("Snack: Protein shake with banana")
        
#         elif fatigue_score >= 200:
#             suggestions['general'].append("Moderate recovery diet")
#             suggestions['macronutrients'] = {
#                 'protein': "1.4-1.6g per kg body weight",
#                 'carbs': "5-6g per kg body weight",
#                 'hydration': "35-45ml per kg body weight"
#             }
#             suggestions['timing'].append("Recovery meal within 2 hours")
#             suggestions['supplements'].append("Optional: Electrolytes, Vitamin C")
        
#         else:
#             suggestions['general'].append("Normal maintenance diet")
#             suggestions['macronutrients'] = {
#                 'protein': "1.2-1.4g per kg body weight",
#                 'carbs': "3-5g per kg body weight",
#                 'hydration': "30-35ml per kg body weight"
#             }
        
#         # Position-specific
#         position = stats.get('position', '').lower()
#         if 'midfielder' in position or 'forward' in position:
#             suggestions['general'].append("Extra carbohydrate loading for endurance")
        
#         if stats.get('sprint_count', 0) > 30:
#             suggestions['supplements'].append("Extra magnesium for muscle recovery")
#             suggestions['supplements'].append("Creatine for explosive power recovery")
        
#         return suggestions  
# modules/recovery_planner.py

class RecoveryPlanner:
    """Generates comprehensive recovery plans based on training dataset patterns"""
    
    def __init__(self):
        print("💊 Initializing Recovery Planner...")
        print("   Loaded recovery protocols for 28 injury types")
        print("   Loaded 8-tier fatigue classification system")
    
    def generate_recovery_plan(self, player_stats, injury_prediction):
        """Creates comprehensive recovery plan"""
        
        # Calculate fatigue score (0-500 scale from training)
        fatigue_score = self._calculate_fatigue_score(player_stats)
        
        # Generate comprehensive plan
        plan = {
            'player_id': player_stats.get('player_id', 'Unknown'),
            'match_date': player_stats.get('match_date', 'Recent Match'),
            
            # Fatigue assessment
            'fatigue_level': self._get_fatigue_level_enhanced(fatigue_score),
            'fatigue_score': int(fatigue_score),
            'fatigue_max': 500,
            
            # Key metrics
            'key_metrics': self._extract_key_metrics(player_stats),
            
            # Position insights
            'position': player_stats.get('position', 'Unknown'),
            'position_insights': self._get_position_insights_enhanced(player_stats),
            
            # Recovery prescription
            'recovery_prescription': self._generate_prescription_enhanced(fatigue_score, injury_prediction, player_stats),
            
            # Warnings
            'warnings': self._generate_warnings_enhanced(injury_prediction, player_stats),
            
            # Recovery timeline
            'timeline': self._generate_recovery_timeline_detailed(fatigue_score, injury_prediction),
            
            # Diet suggestions
            'diet_suggestions': self._generate_diet_suggestions_enhanced(fatigue_score, player_stats)
        }
        
        return plan
    
    def _calculate_fatigue_score(self, stats):
        """Calculate fatigue score (0-500) matching training dataset"""
        score = 0
        
        # Sprints (highly fatiguing)
        score += stats.get('sprint_count', 0) * 3
        
        # Distance (cumulative fatigue)
        score += stats.get('total_distance_km', 0) * 15
        
        # Accelerations (muscle micro-tears)
        score += stats.get('accelerations', 0) * 0.8
        
        # Decelerations (eccentric loading)
        score += stats.get('decelerations', 0) * 1.2
        
        # High speed (muscle strain)
        score += stats.get('max_speed', 0) * 2
        
        # High intensity running
        score += stats.get('high_intensity_distance_km', 0) * 20
        
        return min(score, 500)
    
    def _get_fatigue_level_enhanced(self, score):
        """8-level fatigue classification"""
        if score >= 450:
            return "CRITICAL 🔥🔥🔥"
        elif score >= 400:
            return "CRITICAL 🔥🔥🔥"
        elif score >= 350:
            return "VERY HIGH 🔥🔥"
        elif score >= 300:
            return "HIGH 🔥🔥"
        elif score >= 250:
            return "MODERATE-HIGH 🔥"
        elif score >= 200:
            return "MODERATE 🔥"
        elif score >= 100:
            return "MILD ⚠️"
        else:
            return "LOW ✅"
    
    def _extract_key_metrics(self, stats):
        """Extract key metrics for display"""
        metrics = []
        
        if stats.get('sprint_count', 0) > 0:
            metrics.append(f"{stats['sprint_count']} explosive sprints")
        
        if stats.get('total_distance_km', 0) > 0:
            metrics.append(f"{stats['total_distance_km']:.1f}km total distance")
        
        if stats.get('accelerations', 0) > 0:
            metrics.append(f"{stats['accelerations']} rapid accelerations")
        
        if stats.get('decelerations', 0) > 0:
            metrics.append(f"{stats['decelerations']} hard decelerations")
        
        if stats.get('max_speed', 0) > 0:
            metrics.append(f"{stats['max_speed']:.1f} km/h top speed")
        
        if stats.get('high_intensity_distance_km', 0) > 0:
            metrics.append(f"{stats['high_intensity_distance_km']:.2f}km high-intensity")
        
        return metrics
    
    def _get_position_insights_enhanced(self, stats):
        """Enhanced position-specific insights"""
        position = stats.get('position', '').lower()
        insights = []
        
        if 'goalkeeper' in position:
            insights.append("High-intensity reactions and explosive movements")
            insights.append("Significant shoulder and core loading detected")
            insights.append("Focus on upper body and rotational recovery")
            
        elif 'defender' in position:
            insights.append("High physical contact and dueling detected")
            insights.append("Significant hamstring and knee stress")
            insights.append("Lower body recovery priority")
            
        elif 'midfielder' in position:
            insights.append("Extreme cardiovascular demand detected")
            insights.append("High-volume running with frequent direction changes")
            insights.append("Full-body recovery with cardiovascular focus")
            
        elif 'forward' in position or 'attacking' in position or 'striker' in position or 'winger' in position:
            insights.append("High explosive sprint repetitions")
            insights.append("Significant quadriceps and calf loading")
            insights.append("Focus on lower leg and hamstring recovery")
            
        else:
            insights.append("High-intensity match performance detected")
            insights.append("Full-body recovery recommended")
        
        return insights
    
    def _generate_prescription_enhanced(self, fatigue_score, injury_prediction, stats):
        """Enhanced recovery prescription with detailed protocols"""
        
        # Determine rest days based on 8-level fatigue
        if fatigue_score >= 450:
            rest_days = 5
            hydration = "Drink extra 3.0L+ water today, 2.5L next 2 days"
            sleep = "CRITICAL: 10+ hours for next 5 nights"
            
        elif fatigue_score >= 400:
            rest_days = 4
            hydration = "Drink extra 2.8L water today, 2.3L next 2 days"
            sleep = "Aim for 9.5+ hours for next 4 nights"
            
        elif fatigue_score >= 350:
            rest_days = 3
            hydration = "Drink extra 2.5L water today"
            sleep = "Aim for 9+ hours for next 3 nights"
            
        elif fatigue_score >= 300:
            rest_days = 3
            hydration = "Drink extra 2.0L water today"
            sleep = "Aim for 9+ hours for next 2 nights"
            
        elif fatigue_score >= 250:
            rest_days = 2
            hydration = "Drink extra 1.8L water today"
            sleep = "Aim for 8.5+ hours for next 2 nights"
            
        elif fatigue_score >= 200:
            rest_days = 2
            hydration = "Drink extra 1.5L water today"
            sleep = "Aim for 8+ hours tonight"
            
        elif fatigue_score >= 100:
            rest_days = 1
            hydration = "Drink extra 1.0L water today"
            sleep = "Aim for 8 hours tonight"
            
        else:
            rest_days = 0  # Active recovery
            hydration = "Maintain normal hydration (3L)"
            sleep = "7-8 hours recommended"
        
        # Enhanced activities based on fatigue and injury risk
        activities = []
        position = stats.get('position', '').lower()
        risk_score = injury_prediction.get('raw_risk_score', 0)
        
        if fatigue_score >= 400 or risk_score >= 135:
            activities.append(f"{rest_days} days complete rest - NO training")
            activities.append("Ice bath (10-15 minutes) within 2 hours")
            activities.append("Compression garments 24/7 for first 48h")
            activities.append("Elevation exercises 3x daily")
            activities.append("Professional massage therapy (day 2)")
            if 'midfielder' in position or 'forward' in position:
                activities.append("Full leg compression sleeves")
                activities.append("Consider cryotherapy session")
        
        elif fatigue_score >= 300:
            activities.append(f"{rest_days} days complete rest")
            activities.append("Ice bath (10-15 minutes)")
            activities.append("Compression sleeves recommended")
            activities.append("Foam rolling (full body, 20 mins)")
            activities.append("Light stretching routine (15 mins)")
        
        elif fatigue_score >= 200:
            activities.append("24-48 hours complete rest")
            activities.append("Ice bath or contrast therapy")
            activities.append("Foam rolling (full body)")
            activities.append("Dynamic stretching routine")
        
        else:
            activities.append("Active recovery day")
            activities.append("Light jogging (20-30 mins) or swimming")
            activities.append("Dynamic stretching")
            activities.append("Mobility exercises")
        
        # Nutrition suggestions (enhanced)
        nutrition = []
        if fatigue_score >= 350:
            nutrition.append("CRITICAL: High-carb meal within 30 minutes post-match")
            nutrition.append("Increase protein to 2.0g/kg body weight")
            nutrition.append("Anti-inflammatory supplements (omega-3, turmeric)")
            nutrition.append("Electrolyte drinks every 2 hours for 24h")
        elif fatigue_score >= 250:
            nutrition.append("High-carb meal within 1 hour post-match")
            nutrition.append("Increase protein by 30g/day (1.6-1.8g/kg)")
            nutrition.append("Anti-inflammatory foods (berries, fish)")
        elif fatigue_score >= 150:
            nutrition.append("Balanced post-match meal within 2 hours")
            nutrition.append("Increase protein by 20g/day")
        else:
            nutrition.append("Normal balanced diet")
            nutrition.append("Standard protein intake (1.2-1.4g/kg)")
        
        # Injury-specific nutrition
        if risk_score >= 110:
            nutrition.append("Extra: Collagen peptides, Vitamin D, Magnesium")
        
        return {
            'rest_days': rest_days,
            'hydration': hydration,
            'sleep': sleep,
            'activities': activities,
            'nutrition': nutrition
        }
    
    def _generate_warnings_enhanced(self, injury_prediction, stats):
        """Enhanced warnings with more detail"""
        warnings = []
        
        risk_score = injury_prediction.get('raw_risk_score', 0)
        risk_level = injury_prediction.get('risk_level', '')
        
        # Critical injury risk warnings
        if risk_score >= 160:
            warnings.append(f"CRITICAL injury risk (Level: {risk_level}) - IMMEDIATE medical assessment REQUIRED")
            warnings.append("Do NOT train until cleared by medical staff")
        elif risk_score >= 135:
            warnings.append(f"CRITICAL injury risk ({risk_level}) - Medical consultation strongly advised")
            warnings.append("Minimum 72h rest before any intense activity")
        elif risk_score >= 110:
            warnings.append(f"HIGH injury risk ({risk_level}) - Extra precautions needed")
            warnings.append("48h minimum rest, monitor symptoms closely")
        elif risk_score >= 90:
            warnings.append(f"MODERATE-HIGH injury risk ({risk_level})")
            warnings.append("24h rest minimum, careful progression")
        
        # Specific injury warnings
        for injury in injury_prediction.get('likely_injuries', [])[:3]:
            if injury['probability'] > 0.7:
                warnings.append(f"Very high risk of {injury['type']} ({injury['probability']*100:.0f}%): {', '.join(injury['reasons'])}")
            elif injury['probability'] > 0.5:
                warnings.append(f"High risk of {injury['type']}: {', '.join(injury['reasons'][:2])}")
        
        # Fatigue warnings
        fatigue_score = self._calculate_fatigue_score(stats)
        if fatigue_score > 450:
            warnings.append("EXTREME fatigue detected - Minimum 5 days before next match")
        elif fatigue_score > 400:
            warnings.append("Critical fatigue - Minimum 4 days recovery needed")
        elif fatigue_score > 350:
            warnings.append("Very high fatigue - 72h minimum before next intense match")
        elif fatigue_score > 300:
            warnings.append("High fatigue - Allow 48-72h recovery")
        elif fatigue_score > 250:
            warnings.append("Moderate-high fatigue - 48h minimum recovery")
        
        # Position-specific warnings
        position = stats.get('position', '').lower()
        if stats.get('sprint_count', 0) > 40:
            warnings.append("Extremely high sprint count - Monitor hamstring tightness closely")
        
        if stats.get('total_distance_km', 0) > 13:
            warnings.append("Excessive distance covered - Risk of overuse injuries")
        
        if 'midfielder' in position and fatigue_score > 300:
            warnings.append("High cardiovascular load - Heart rate monitoring recommended")
        
        return warnings
    
    def _generate_recovery_timeline_detailed(self, fatigue_score, injury_prediction):
        """Detailed 7-day recovery timeline"""
        timeline = []
        risk_score = injury_prediction.get('raw_risk_score', 0)
        
        if fatigue_score >= 450 or risk_score >= 160:
            timeline = [
                "Day 0 (Today): Complete rest + ice bath + compression + elevation",
                "Day 1: Complete rest + hydration focus + professional massage",
                "Day 2: Complete rest + gentle passive stretching (10 mins)",
                "Day 3: Light walking (15-20 mins) + foam rolling",
                "Day 4: Light walking (20-30 mins) + dynamic stretching",
                "Day 5: 30% training intensity + monitor symptoms",
                "Day 6: 50% training intensity if pain-free",
                "Day 7: Medical clearance check before progression"
            ]
        elif fatigue_score >= 400 or risk_score >= 135:
            timeline = [
                "Day 0: Complete rest + ice bath + compression",
                "Day 1: Complete rest + hydration + light stretching",
                "Day 2: Light walking (20 mins) + foam rolling",
                "Day 3: Light jog (20 mins, 60% intensity) + stretching",
                "Day 4: 50% training intensity",
                "Day 5: 70% training intensity",
                "Day 6: 85% training intensity",
                "Day 7: Full clearance expected (if symptom-free)"
            ]
        elif fatigue_score >= 350:
            timeline = [
                "Day 0: Complete rest + ice bath",
                "Day 1: Light walking (25 mins) + foam rolling",
                "Day 2: Light jog (25 mins) + dynamic stretching",
                "Day 3: 60% training intensity",
                "Day 4: 80% training intensity",
                "Day 5: Full clearance expected"
            ]
        elif fatigue_score >= 300:
            timeline = [
                "Day 0: Active recovery + hydration",
                "Day 1: Light jog (30 mins) + stretching",
                "Day 2: 70% training intensity",
                "Day 3: 90% training intensity",
                "Day 4: Full clearance expected"
            ]
        elif fatigue_score >= 200:
            timeline = [
                "Day 0: Active recovery + hydration",
                "Day 1: Light jog (30 mins)",
                "Day 2: 80% training intensity",
                "Day 3: Full clearance expected"
            ]
        else:
            timeline = [
                "Day 0: Normal recovery + hydration",
                "Day 1: Return to full training"
            ]
        
        # Add injury-specific adjustments
        if risk_score >= 135:
            timeline.insert(0, "⚕️ Medical consultation required before starting timeline")
        
        return timeline
    
    def _generate_diet_suggestions_enhanced(self, fatigue_score, stats):
        """Enhanced diet suggestions"""
        suggestions = {
            'general': [],
            'macronutrients': {},
            'timing': [],
            'supplements': [],
            'sample_meals': []
        }
        
        if fatigue_score >= 400:
            suggestions['general'].append("HIGH-CALORIE recovery diet essential")
            suggestions['general'].append("Focus on nutrient timing for optimal recovery")
            suggestions['macronutrients'] = {
                'protein': "2.0-2.2g per kg body weight",
                'carbs': "8-10g per kg body weight",
                'fats': "1.0-1.2g per kg body weight",
                'hydration': "50-60ml per kg body weight"
            }
            suggestions['timing'].append("Post-match meal within 30 minutes (carb+protein 4:1)")
            suggestions['timing'].append("Protein-rich snack every 3 hours")
            suggestions['timing'].append("Pre-sleep protein (casein) for muscle repair")
            suggestions['supplements'].append("CRITICAL: Whey protein, BCAAs, Electrolytes")
            suggestions['supplements'].append("Anti-inflammatory: Omega-3, Turmeric")
            suggestions['supplements'].append("Recovery: Vitamin D, Magnesium, Zinc")
            suggestions['sample_meals'].append("Post-match: Rice bowl with chicken, sweet potato")
            suggestions['sample_meals'].append("2h later: Greek yogurt with berries and honey")
            suggestions['sample_meals'].append("Dinner: Salmon, quinoa, vegetables")
        
        elif fatigue_score >= 300:
            suggestions['general'].append("High-calorie recovery diet recommended")
            suggestions['macronutrients'] = {
                'protein': "1.6-2.0g per kg body weight",
                'carbs': "6-8g per kg body weight",
                'hydration': "40-50ml per kg body weight"
            }
            suggestions['timing'].append("Post-match meal within 1 hour")
            suggestions['timing'].append("Small meals every 3-4 hours")
            suggestions['supplements'].append("Whey protein, BCAAs, Electrolytes")
            suggestions['supplements'].append("Consider: Omega-3, Vitamin C")
            suggestions['sample_meals'].append("Post-match: Pasta with lean meat")
            suggestions['sample_meals'].append("Snack: Protein shake with banana")
        
        elif fatigue_score >= 200:
            suggestions['general'].append("Moderate recovery diet")
            suggestions['macronutrients'] = {
                'protein': "1.4-1.6g per kg body weight",
                'carbs': "5-6g per kg body weight",
                'hydration': "35-45ml per kg body weight"
            }
            suggestions['timing'].append("Recovery meal within 2 hours")
            suggestions['supplements'].append("Optional: Electrolytes, Vitamin C")
        
        else:
            suggestions['general'].append("Normal maintenance diet")
            suggestions['macronutrients'] = {
                'protein': "1.2-1.4g per kg body weight",
                'carbs': "3-5g per kg body weight",
                'hydration': "30-35ml per kg body weight"
            }
        
        # Position-specific
        position = stats.get('position', '').lower()
        if 'midfielder' in position or 'forward' in position:
            suggestions['general'].append("Extra carbohydrate loading for endurance")
        
        if stats.get('sprint_count', 0) > 30:
            suggestions['supplements'].append("Extra magnesium for muscle recovery")
            suggestions['supplements'].append("Creatine for explosive power recovery")
        
        return suggestions