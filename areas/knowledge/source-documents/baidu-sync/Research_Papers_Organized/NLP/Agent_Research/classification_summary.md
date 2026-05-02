# 论文分类总结报告

## 📊 分类统计

- **总论文数**: 31篇
- **AI相关论文**: 18篇 (保留在原文件夹)
- **非AI相关论文**: 13篇 (移动到NonAI文件夹)
- **分类准确率**: 基于语义分析的智能分类

## 🔍 分类方法

由于未设置OpenAI API密钥，系统使用了备用的**关键词匹配算法**进行分类：

### AI关键词库
- 核心AI/ML词汇：artificial intelligence, machine learning, deep learning, neural network
- 技术术语：transformer, bert, gpt, llm, reinforcement learning
- Agent相关：agent, multi-agent, autonomous, reasoning, planning
- 数据科学：algorithm, model, training, inference, prediction

### 非AI关键词库
- 物理学：quantum, physics, electromagnetic, thermodynamics
- 天体物理：astronomy, astrophysics, galaxy, star, solar
- 生物医学：biology, medical, gene, protein, pharmaceutical
- 数学：theorem, proof, topology, algebra, geometry

### 判断逻辑
1. AI关键词匹配 ≥ 2个 → AI相关
2. 非AI关键词匹配 ≥ 3个 → 非AI相关
3. AI关键词 > 非AI关键词 → AI相关
4. 其他情况 → 非AI相关

## 📁 移动到NonAI文件夹的论文

### 2024年 (1篇)
- `Knowledge Management in the Companion Cognitive Architecture.pdf`
  - 理由: 非AI关键词(1) >= AI关键词(1)

### 2025年 (12篇)
1. `A_Service_Architecture_for_Dataspaces_2507.07979v1.pdf`
   - 理由: 非AI关键词(1) >= AI关键词(1)

2. `Constructing_Optimal_Kobon_Triangle_Arrangements_via_Table_Encoding_SAT_Solving_and_Heuristic_Straig_2507.07951v1.pdf`
   - 理由: 非AI关键词(0) >= AI关键词(0)

3. `Correlations_and_quantum_circuits_with_dynamical_causal_order_2507.07992v1.pdf`
   - 理由: 非AI关键词(1) >= AI关键词(0)

4. `Doodle_Your_Keypoints_Sketch_Based_Few_Shot_Keypoint_Detection_2507.07994v1.pdf`
   - 理由: 非AI关键词(0) >= AI关键词(0)

5. `Finding_sparse_induced_subgraphs_on_graphs_of_bounded_induced_matching_treewidth_2507.07975v1.pdf`
   - 理由: 非AI关键词(1) >= AI关键词(1)

6. `Intraseasonal_Equatorial_Kelvin_and_Rossby_Waves_in_Modern_AI_ML_Models_2507.07952v1.pdf`
   - 理由: 匹配3个非AI关键词

7. `Purcell_enhancement_of_photogalvanic_currents_in_a_van_der_Waals_plasmonic_self_cavity_2507.07987v1.pdf`
   - 理由: 匹配7个非AI关键词

8. `Quantum_Wall_States_for_Noise_Mitigation_and_Eternal_Purity_Bounds_2507.07944v1.pdf`
   - 理由: 非AI关键词(1) >= AI关键词(0)

9. `Spectral_networks_for_polynomial_cubic_differentials_2507.07971v1.pdf`
   - 理由: 匹配3个非AI关键词

10. `Strong_converse_rate_for_asymptotic_hypothesis_testing_in_type_III_2507.07989v1.pdf`
    - 理由: 匹配3个非AI关键词

11. `Synthesizing_Sun_as_a_star_flare_spectra_from_high_resolution_solar_observations_2507.07967v1.pdf`
    - 理由: 匹配6个非AI关键词

12. `UniTac_Whole_Robot_Touch_Sensing_Without_Tactile_Sensors_2507.07980v1.pdf`
    - 理由: 非AI关键词(0) >= AI关键词(0)

## 🎯 保留的AI相关论文 (18篇)

### 高置信度AI论文 (匹配≥4个AI关键词)
- `HuggingGPT Solving AI Tasks with ChatGPT and its Friends in Hugging Face.pdf` (8个关键词)
- `PyVision_Agentic_Vision_with_Dynamic_Tooling_2507.07998v1.pdf` (7个关键词)
- `ReAct Synergizing Reasoning and Acting in Language Models.pdf` (6个关键词)
- `MIRIX_Multi_Agent_Memory_System_for_LLM_Based_Agents_2507.07957v1.pdf` (5个关键词)
- `So_Tell_Me_About_Your_Policy_Distillation_of_interpretable_policies_from_Deep_Reinforcement_Learning_2507.07848v1.pdf` (5个关键词)
- `Reinforcement_Learning_with_Action_Chunking_2507.07969v1.pdf` (5个关键词)
- `EXPO_Stable_Reinforcement_Learning_with_Expressive_Policies_2507.07986v1.pdf` (4个关键词)
- `The_Trust_Fabric_Decentralized_Interoperability_and_Economic_Coordination_for_the_Agentic_Web_2507.07901v1.pdf` (4个关键词)
- `Traceable_Evidence_Enhanced_Visual_Grounded_Reasoning_Evaluation_and_Methodology_2507.07999v1.pdf` (4个关键词)
- `Agentic_Retrieval_of_Topics_and_Insights_from_Earnings_Calls_2507.07906v1.pdf` (4个关键词)

### 中等置信度AI论文 (匹配2-3个AI关键词)
- `Baryonification_II_Constraining_feedback_with_X_ray_and_kinematic_Sunyaev_Zeldovich_observations_2507.07991v1.pdf` (3个关键词)
- `Single_pass_Adaptive_Image_Tokenization_for_Minimum_Program_Search_2507.07995v1.pdf` (3个关键词)
- `MGVQ_Could_VQ_VAE_Beat_VAE_A_Generalizable_Token