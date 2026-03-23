



import pandas as pd

import seaborn as sns

import matplotlib.pyplot as plt

import matplotlib as mpl

import scipy.stats as stats

import numpy as np

from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split, cross_validate, cross_val_score, ShuffleSplit,cross_validate

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, roc_auc_score, auc

from sklearn.decomposition import PCA

from imblearn.over_sampling import SVMSMOTE

from joblib import dump, load

from pathlib import Path

import os







mpl.set_loglevel("debug")

font_paths = mpl.font_manager.findSystemFonts()

for font_file in font_paths:

  mpl.font_manager.fontManager.addfont(font_file)



plt.rcParams['font.family'] = 'Arial'

plt.rcParams['font.sans-serif'] = 'Arial'

plt.rcParams['font.size'] = 10

plt.rcParams['figure.figsize'] = (3.1, 3)



sns.set_theme(style="white", rc={"grid.linewidth": 0.1, 'figure.figsize':(3.1,3)})

sns.set_style("ticks")

sns.set(font='Arial')

sns.set_context("paper", font_scale=0.9)

plt.figure(figsize=(3.1, 3))

#sns.despine(left=False, bottom=False)



def save_figure(fig,name):

  prefix = './outputs/images/'

  svg_prefix = f'{prefix}svg/'

  png_prefix = f'{prefix}png/'

  eps_prefix = f'{prefix}eps/'

  pdf_prefix = f'{prefix}pdf/'

  prefixs = [svg_prefix, png_prefix, eps_prefix, pdf_prefix]

  prefixs_names = ['svg', 'png', 'eps', 'pdf']

  for p in prefixs:

    Path(p).mkdir(parents=True, exist_ok=True)

  for i in range(len(prefixs)):

    fig.savefig(f'{prefixs[i]}{name}.{prefixs_names[i]}', format=prefixs_names[i], bbox_inches='tight', dpi=300)





FILES_PATHS = ['https://raw.githubusercontent.com/fez2010/tp_map6014/refs/heads/main/datasets/turnover.csv','https://raw.githubusercontent.com/fez2010/tp_map6014/refs/heads/main/datasets/turnover_prepared.csv']

datasets = []

for path in FILES_PATHS:

  #get csv file encoding

  df = pd.read_csv(path, encoding='Latin-1')



  df.columns = df.columns.str.capitalize()

  datasets.append(df)



print(datasets[1].shape)

datasets[0].head()



# Creation des ensembles de nom

CATEGORY_COLUMNS= ['Industry', 'Profession','Traffic', 'Coach', 'Head_gender','Greywage','Way','Gender']

QUANTITATIVE_COLUMNS = ['Age','Stag','Novator','Anxiety','Selfcontrol','Independ','Extraversion','Wayencoded']

REAL_QUANTITATIVE_COLUMNS = ['Stag', 'Novator','Anxiety','Selfcontrol','Independ','Extraversion']

INTEGER_QUANTITATIVE_COLUMNS = ['Age']

# Liste des variables explicatives

EXPLICATIVES_COLUMNS = CATEGORY_COLUMNS + QUANTITATIVE_COLUMNS

# Classe Cible

TARGET = 'Event'

# Codes Couleur

COLOR_PALETTE = ['#8B383F','#373D61','#203AE0']



print(datasets[0].isnull().sum())





print(datasets[1].isnull().sum())



for column in CATEGORY_COLUMNS:

  print(f'Les valeurs de la colonne {column} sont : ',', '.join(datasets[0][column].unique()))





def get_description(dataset):

  description = dataset.describe(include='all')

  description = dataset.describe(include='all')

  description.loc['var'] = dataset.var().tolist()

  description.loc['skew'] = dataset.skew().tolist()

  description.loc['kurt'] = dataset.kurtosis().tolist()

  return description

print(get_description(datasets[1]))

stats.normaltest(datasets[1][TARGET])



data = datasets[1][TARGET].value_counts()



data.values





# Graphe de la repartion des données par classe

with sns.axes_style("ticks"):

  splot = plt.pie(data, labels=['Rotation', 'Pas de rotation'], colors=COLOR_PALETTE, autopct='%.0f%%')

  plt.xticks(rotation=90)

  plt.tight_layout()

  plt.title('Répartition des données par classes')

  plt.show()

  save_figure(plt, 'dataset_pie_chart')







with sns.axes_style("ticks"):

  for column in INTEGER_QUANTITATIVE_COLUMNS:

    splot = sns.displot(

        datasets[1],

        x=column, hue=TARGET,

        multiple="stack",

        palette=COLOR_PALETTE,

        edgecolor=".3",

        linewidth=.7,

        stat="probability",

        log_scale=False,

    )



    x_ticks = [int(x) for x in datasets[1][column].unique()]

    splot.ax.set_xticks( [min(x_ticks), int(datasets[1][column].mean()) ,max(x_ticks)])

    plt.axvline(datasets[1][column].median(), color=COLOR_PALETTE[2],linestyle='--', label='Médiane')

    splot.legend.remove()

    splot.ax.set_ylabel("Probabilité")

    splot.ax.set_xlabel("")

    splot.ax.set_title(f"Distribution des valeurs de la colonne {column}")

    plt.show()

    save_figure(splot, f'distribution_{column}')



with sns.axes_style("ticks"):

  for column in REAL_QUANTITATIVE_COLUMNS:

    plt.figure(figsize=(3.1, 3))

    splot = sns.displot(data=datasets[1], x=column, kind="kde",palette=COLOR_PALETTE,  bw_adjust=.25)



    plt.legend().remove()

    x_ticks = [int(x) for x in datasets[1][column].unique()]

    splot.ax.set_xticks( [min(x_ticks), int(datasets[1][column].mean()) ,max(x_ticks)])

    plt.axvline(datasets[1][column].median(), color=COLOR_PALETTE[2],linestyle='--', label='Médiane')

    splot.ax.set_ylabel("Densité")

    splot.ax.set_xlabel("")

    splot.ax.set_title(f"Distribution de la densité des valeurs de la colonne {column}")

    plt.show()

    save_figure(splot, f'density_distribution_{column}')





scaler = StandardScaler()

f_scaler = scaler

b = datasets[1].copy()

b[EXPLICATIVES_COLUMNS] = scaler.fit_transform(b[EXPLICATIVES_COLUMNS])



with sns.axes_style("ticks"):

  b[QUANTITATIVE_COLUMNS].boxplot(figsize=(3.1, 3))

  plt.xticks(rotation=90)

  plt.title('Identification des colonnes présentant des anomalies')

  plt.show()

  save_figure(plt, f'main_boxplot_show_outlier_columns')





IQR_dataset = b.copy()



# Colonnes présentant des outliers

columns = ['Stag','Age']

with sns.axes_style("ticks"):

      IQR_dataset[columns].boxplot(figsize=(3.1, 3))

      plt.xticks(rotation=90)

      plt.show()

      save_figure(plt, f'boxplot_show_outlier_column_{column}')

def remove_outliers(IQR_dataset, columns):

  for column in columns:

    # IQR

    Q1 = np.percentile(IQR_dataset[column], 25, method='midpoint')

    Q3 = np.percentile(IQR_dataset[column], 75, method='midpoint')

    IQR = Q3 - Q1

    print(f"IQR de la colonne {column} ", IQR)



    # Limite superieur

    upper = Q3+1.5*IQR

    upper_array = np.array(IQR_dataset[column] >= upper)

    print(f"Limite superieur de la colonne {column}:", upper)

    print(upper_array.sum())



    # Limite inferieur

    lower = Q1-1.5*IQR

    lower_array = np.array(IQR_dataset[column] <= lower)

    print(f"Limite inferieur de la colonne {column}:", lower)

    print(lower_array.sum())





    # Creation du tableau Boolean indiquant les lignes ayant des outliers

    upper_array = np.where(IQR_dataset[column] >= upper)[0]

    lower_array = np.where(IQR_dataset[column] <= lower)[0]

    with sns.axes_style("ticks"):

      IQR_dataset[[column]].boxplot(figsize=(3.1, 3))

      plt.xticks(rotation=90)

      plt.axhline(upper, color='red', linestyle='--', label='Limite superieur')

      plt.axhline(lower, color='red', linestyle='--', label='Limite inferieur')

      plt.legend()

      plt.show()

      save_figure(plt, f'boxplot_show_outlier_column_{column}')

    # Suppression des outliers

    IQR_dataset.drop(index=upper_array, inplace=True)

    IQR_dataset.drop(index=lower_array, inplace=True)

    IQR_dataset.reset_index(drop=True, inplace=True)

    # Afficher la nouvelle taille du  DataFrame

    print(f"Nouvelle taille apres suppression des outliers sur la colonne {column}: ", IQR_dataset.shape)



  return IQR_dataset

IQR_dataset = remove_outliers(IQR_dataset, columns)

#IQR_dataset = remove_outliers(IQR_dataset, columns)

#IQR_dataset = remove_outliers(IQR_dataset, columns)

with sns.axes_style("ticks"):

      IQR_dataset[columns].boxplot(figsize=(3.1, 3))

      plt.xticks(rotation=90)

      plt.show()

      save_figure(plt, f'boxplot_show_outlier_removed_on_columns')



with sns.axes_style("ticks"):

  IQR_dataset[QUANTITATIVE_COLUMNS].boxplot(figsize=(3.1, 3))

  plt.xticks(rotation=90)

  #plt.tight_layout()

  plt.show()

  save_figure(plt, f'main_boxplot_show_outlier_removed_on_columns')



IQR_dataset.shape



with sns.axes_style("ticks"):

  plt.figure(figsize=(13, 6))

  mask = np.triu(np.ones_like(IQR_dataset.corr()))

  mask[0][0] = False

  mask[mask.shape[0]-1][mask.shape[1]-1] = False

  heatmap = sns.heatmap(IQR_dataset.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')

  plt.tight_layout()

  plt.box(False)

  plt.show()

  save_figure(plt, 'corr_heatmap_after_removing_outlier')





ZScore_dataset = datasets[1].copy()



ZScore_dataset[EXPLICATIVES_COLUMNS] = scaler.fit_transform(ZScore_dataset[EXPLICATIVES_COLUMNS])

with sns.axes_style("ticks"):

  ZScore_dataset[QUANTITATIVE_COLUMNS].boxplot()

  plt.xticks(rotation=90)

  plt.show()



age_threshold_z = datasets[1]['Age'].std() * 2.8



outlier_indices = np.where(ZScore_dataset['Stag'] > 2.2)[0]

print(outlier_indices)

no_outliers = ZScore_dataset.drop(outlier_indices)

print("Original DataFrame Shape:", ZScore_dataset.shape)

print("DataFrame Shape after Removing Outliers:", no_outliers.shape)



with sns.axes_style("ticks"):

  no_outliers[QUANTITATIVE_COLUMNS].boxplot()

  plt.xticks(rotation=90)

  plt.show()

no_outliers.reset_index(drop=True, inplace=True)



threshold_z = 2.8



outlier_indices = np.where(no_outliers['Age'] > threshold_z)[0]

print(outlier_indices, )

no_outliers_2 = no_outliers.drop(outlier_indices)

print("Original DataFrame Shape:", no_outliers.shape)

print("DataFrame Shape after Removing Outliers:", no_outliers_2.shape)



with sns.axes_style("ticks"):

  no_outliers_2[QUANTITATIVE_COLUMNS].boxplot()

  plt.xticks(rotation=90)

  plt.show()





no_outliers_2.shape



with sns.axes_style("ticks"):

  plt.figure(figsize=(13, 6))

  # define the mask to set the values in the upper triangle to True

  mask = np.triu(np.ones_like(no_outliers_2.corr()))

  mask[0][0] = False

  mask[mask.shape[0]-1][mask.shape[1]-1] = False

  heatmap = sns.heatmap(no_outliers_2.corr(), mask=mask, vmin=-1, vmax=1, annot=True, cmap='BrBG')

  heatmap.bbox_inches = 'with'

  plt.tight_layout()

  plt.box(False)

  plt.show()

  plt.savefig('out_main_headmap.png')



REMOVED_COLUMNS = ['Wayencoded']

CATEGORY_COLUMNS= ['Industry', 'Profession','Traffic', 'Coach', 'Head_gender','Greywage','Way','Gender']

QUANTITATIVE_COLUMNS = ['Age','Stag','Novator','Anxiety','Selfcontrol','Independ','Extraversion']

EXPLICATIVES_COLUMNS = CATEGORY_COLUMNS + QUANTITATIVE_COLUMNS

IQR_dataset = IQR_dataset[EXPLICATIVES_COLUMNS + [TARGET]]

no_outliers_2 = no_outliers_2[EXPLICATIVES_COLUMNS + [TARGET]]



print(IQR_dataset.shape)

print(no_outliers_2.shape)

IQR_dataset.head()

assert IQR_dataset.shape[1] == no_outliers_2.shape[1] == datasets[1].shape[1] - len(REMOVED_COLUMNS)



ACP_dataset = IQR_dataset.copy()



def generate_components_short_names(n):

  return [f'C{i+1}' for i in range(n)]



# Créer un objet PCA

pca = PCA(random_state=0)



# Appliquer l'ACP aux données standardisées

pca.fit(ACP_dataset[EXPLICATIVES_COLUMNS])



# Composantes principales

components = pca.components_



# Variance expliquée

explained_variance = pca.explained_variance_ratio_



# Matrice des valeurs propres (Importance des facteurs)

eigenvalues = pca.explained_variance_



# Vecteurs propres (Construction des facteurs)

eigenvectors = pca.components_



# Contributions des variables aux composantes principales 1 et 2

contributions = pca.components_[:2, :].T



# Noms des variables

variable_names = ACP_dataset[EXPLICATIVES_COLUMNS].columns



# Matrice des valeurs propres

# Saturations (Importance des variables / facteurs)

loadings = eigenvectors * np.sqrt(eigenvalues.reshape(-1, 1))

with sns.axes_style("ticks"):

  # Créez un graphique de dispersion des contributions

  plt.figure(figsize=(10, 6))

  plt.scatter(contributions[:, 0], contributions[:, 1], marker='o', color='blue', alpha=0.5)

  plt.xlabel('Contribution à C1')

  plt.ylabel('Contribution à C2')

  save_figure(plt, f'dispertion_of_variable_contribution_to_composent_one_and_two')



  # Ajoutez les noms des variables

  for i, variable in enumerate(variable_names):

      plt.annotate(variable, (contributions[i, 0], contributions[i, 1]))



  plt.title('Contributions des Variables aux Composantes Principales 1 et 2')

  plt.grid(color='white', linestyle='--', linewidth=0.5)

  plt.box(False)

  plt.axhline(0, color='black', linewidth=0.5)

  plt.axvline(0, color='black', linewidth=0.5)

  plt.show()

  save_figure(plt, f'variable_contribution_to_composent_one_and_two')



  # Visualisation des valeurs propres par pourcentage expliquer

  plt.figure(figsize=(3.1, 3))

  plt.bar(range(1, len(eigenvalues) + 1), explained_variance *100, alpha=0.5, align='center')

  plt.axhline(1, color='red', linestyle='--', label="Seuil de signifiance")

  plt.xlabel('Composante Principale')

  plt.ylabel('Valeur Propre')

  plt.grid(color='gray', linestyle='--', linewidth=0.5)

  plt.show()

  save_figure(plt, f'bar_show_prinpal_components')

  # Visualisation des valeurs propres

  plt.figure(figsize=(3.1, 3))

  plt.bar(range(1, len(eigenvalues) + 1), eigenvalues, alpha=0.5, align='center')

  plt.axhline(1, color='red', linestyle='--', label="Seuil d'importance")

  plt.xlabel('Composante Principale')

  plt.ylabel('Valeur Propre')

  plt.grid(color='gray', linestyle='--', linewidth=0.5)

  plt.show()

  save_figure(plt, f'bar_show_principal_component_column_{column}')

pd.DataFrame(data = { 'TVE': eigenvalues, 'PVTE': explained_variance*100, 'CumPVTE': np.cumsum(explained_variance*100) },  index=generate_components_short_names(len(eigenvalues)))













# Nombre de composantes choisie

n = 7

pca = PCA(n_components=n, random_state=0)

sm = SVMSMOTE(random_state=0)



# Appliquer l'ACP aux données standardisées



reduced_ACP_dataset = pca.fit_transform(ACP_dataset[EXPLICATIVES_COLUMNS])

reduced_ACP_dataset = pd.DataFrame(data=reduced_ACP_dataset, columns=generate_components_short_names(n))

reduced_ACP_dataset[TARGET] = ACP_dataset[TARGET]



# Composantes principales

components = pca.components_



# Corretion du déséquilibre

X, y = sm.fit_resample(reduced_ACP_dataset[generate_components_short_names(n)], reduced_ACP_dataset[TARGET])

print(X.shape)

# Diviser le dataset en ensembles d'entraînement et de test

cv = ShuffleSplit(n_splits=500, test_size=0.3, random_state=0)



# Créer un modèle de régression logistique avec régularisation L2 (Ridge)

alpha = 1  # Paramètre de régularisation, ajustez selon vos besoins

model = LogisticRegression( penalty='l2', solver='newton-cg', random_state=0, C=1/alpha, max_iter=1000)



scoring = ['precision_micro', 'roc_auc','recall','accuracy','f1_micro']

# Entraîner le modèle sur les données d'entraînement

scores = cross_validate(model, X, y, cv=cv, scoring=scoring,return_train_score=True, return_estimator=True,  return_indices=True)

print(scores.keys(),"%0.2f accuracy with a standard deviation of %0.2f" % (scores['test_accuracy'].mean(), scores['test_roc_auc'].std()))



# Sélection du meilleur estimateur (test_recall, test_f1_micro, test_precision_micro, test_accuracy, test_roc_auc)

index = [np.where(scores['test_recall']==scores['test_recall'].max())[0],np.where(scores['test_f1_micro']==scores['test_f1_micro'].max())[0],np.where(scores['test_precision_micro']==scores['test_precision_micro'].max())[0], np.where(scores['test_accuracy']==scores['test_accuracy'].max())[0],np.where(scores['test_roc_auc']==scores['test_roc_auc'].max())[0]]

print(index)



















Index = np.concatenate(index)

Index = np.unique(np.array(Index.tolist(), dtype=np.int16)).tolist()

def generate_estimator_short_names(n):

  return [f'E{i+1}' for i in range(n)]



estimators_names = generate_estimator_short_names(len(Index))

Metrics = ['test_recall', 'test_f1_micro', 'test_precision_micro', 'test_accuracy', 'test_roc_auc']

Performances = {'#Indices': []}

for i in range(len(Metrics)):

  Performances[Metrics[i]] = []

  for j in range(len(Index)):

    Performances[Metrics[i]].append(scores[Metrics[i]][Index[j]])

    Performances['#Indices'].append(Index[j])

es = pd.DataFrame(Performances,columns=Metrics, index=estimators_names)

es.columns =  es.columns.str.capitalize()

es.columns =  es.columns.str.replace('_', ' ')

es['#Indice'] = Index

es





# Prendre l'estimateur qui a la meilleur courbe roc



def get_roc_auc(scores, index, Fclass):

  model = scores['estimator'][index]

  X_test = X.iloc[scores['indices']['test'][index]]

  y_test = y.iloc[scores['indices']['test'][index]]

  y_pred_proba = model.predict_proba(X_test)[:, 1]

  fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

  roc_auc = auc(fpr, tpr)

  return fpr, tpr, thresholds, roc_auc

with sns.axes_style("ticks"):

  plt.figure(figsize=(3.1, 3))

  for index in range(len(Index)):

    fpr, tpr, thresholds, roc_auc = get_roc_auc(scores, Index[index], 1)



    plt.plot(fpr, tpr,  lw=2, label=f'ROC {estimators_names[index]} (area = %0.2f)' % roc_auc)

  plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')

  plt.xlim([0.0, 1.0])

  plt.ylim([0.0, 1.05])

  plt.xlabel('Taux de FP')

  plt.ylabel('Taux de VP')

  plt.title('Courbe ROC')

  plt.legend(loc="lower right")

  plt.show()

  save_file(plt, 'roc_curve')



model = scores['estimator'][Index[1]]

X_test = X.iloc[scores['indices']['test'][Index[1]]]

y_test = y.iloc[scores['indices']['test'][Index[1]]]



# Faire des prédictions sur l'ensemble de test

y_pred = model.predict(X_test)



# Calculer les métriques de performance

accuracy = accuracy_score(y_test, y_pred)

conf_matrix = confusion_matrix(y_test, y_pred)

class_report = classification_report(y_test, y_pred)



# Afficher les métriques de performance

print("Accuracy:", accuracy)

print("Confusion Matrix:\n", conf_matrix)

print("Classification Report:\n", class_report)



group_names = ['TN','FP','FN','VP']

group_counts = ["{0:0.0f}".format(value) for value in conf_matrix.flatten()]

group_percentages = ['{0:.2%}'.format(value) for value in conf_matrix.flatten()/np.sum(conf_matrix)]

labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]

labels = np.asarray(labels).reshape(2,2)

with sns.axes_style("ticks"):



  splot = sns.heatmap(conf_matrix, annot=labels, fmt='', cmap='Blues')

  save_figure(plt,'matrice_confusion_meilleur_estimateur')



# Sauvegarde des models

Path("./outputs/models/").mkdir(parents=True, exist_ok=True)

dump(model, './outputs/models/model.joblib')

dump(f_scaler, './outputs/models/scaler.joblib')

dump(pca, './outputs/models/pca.joblib')

with open('./outputs/models/model_input_columns_name.txt', 'w') as f:

  f.write(','.join(EXPLICATIVES_COLUMNS + REMOVED_COLUMNS))

with open('./outputs/models/model_pca_input_columns_name.txt', 'w') as f:

  f.write(','.join(EXPLICATIVES_COLUMNS ))



# Test du chargement des Models et Prediction

input_columns = []

pca_input_columns = []

with open('./outputs/models/model_input_columns_name.txt', 'r') as f:

  f.seek(0)

  input_columns = f.read().split(',')

with open('./outputs/models/model_pca_input_columns_name.txt', 'r') as f:

  f.seek(0)

  pca_input_columns = f.read().split(',')

model = load('./outputs/models/model.joblib')

scaler = load('./outputs/models/scaler.joblib')

pca = load('./outputs/models/pca.joblib')

X_test = datasets[1][input_columns].iloc[1:10]

X_test[input_columns] = scaler.transform(datasets[1][input_columns].iloc[1:10])

X_test_r = pca.transform(X_test[pca_input_columns])

y_pred = model.predict(X_test_r)

y_pred_proba = model.predict_proba(X_test_r)

print(y_pred, y_pred_proba)
