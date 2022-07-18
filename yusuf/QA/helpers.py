#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 16:18:27 2017

@author: yusuf
"""

def fdr(pvalues, correction_type='Benjamini-Hochberg'):
    """
    fdr(pvalues, correction_type='Benjamini-Hochberg'):
    
    Returns an adjusted pvalue array same shape as the input.
    
    http://stackoverflow.com/questions/7450957/how-to-implement-rs-p-adjust-in-python
    """
    import numpy as np
    #retain a copy of the data for reshaping to original format
    pvalues_orig=np.array(pvalues)
    pvalues_out=np.ones((np.size(pvalues_orig),))  #1d array
    
    #grab only those p-values that are not exactly equal to 1
    # (pvalues are 1 when the model was not fit and the element was skipped over)
    w=np.where(pvalues_orig.flatten()<1)[0]
    pvalues=pvalues_orig[pvalues_orig<1]  #flattens
    
    n=float(pvalues.shape[0])
    new_pvalues=np.empty(int(n))
    if correction_type=='Bonferroni':
        new_pvalues=n*pvalues
        new_pvalues[new_pvalues>1]=1
    elif correction_type=='Bonferroni-Holm':
        values=[(pvalue,i) for i,pvalue in enumerate(pvalues)]
        values.sort()
        for rank,vals in enumerate(values):
            new_pvalues[vals[1]]=(n-rank)*vals[0]
    elif correction_type=='Benjamini-Hochberg':
        values=[(pvalue,i) for i,pvalue in enumerate(pvalues)]
        values.sort()
        values.reverse()
        new_values=[]
        for i,vals in enumerate(values):
            rank=n-i
            pvalue,index=vals
            new_values.append((n/rank)*pvalue)
        for i in range(0,int(n)-1):
            if new_values[i] < new_values[i+1]:
                new_values[i+1]=new_values[i]
        for i,vals in enumerate(values):
            new_pvalues[vals[1]]=new_values[i]
    
    #fill in values
    pvalues_out[w]=new_pvalues
    
    return pvalues_out.reshape(pvalues_orig.shape)

def savetxt_compact(fname, mat, fmt="%.6f", delimiter=' ', fileAccessMode='a'):
    with open(fname, fileAccessMode) as fh:
        for row in mat:
            line = delimiter.join("0" if value == 0 else fmt % value for value in row)
            fh.write(line + '\n')

def calculateZScore(data,controlGroupOrder):
    import numpy as np
    
    newData=np.zeros(data.shape)
    for i in range(len(data)):
        if(i<len(controlGroupOrder)):
            controls=np.delete(controlGroupOrder,i)
        meanControl = np.mean(data[controls])
        stdControl = np.std(data[controls])
        newData[i] = (data[i]-meanControl)/stdControl
    return newData

def removeOutliers(data):
    import numpy as np
    
    q1,q3 = np.percentile(sorted(data),[25,75])
    iqr = q3-q1
    lowerBound = q1 - (1.5*iqr)
    upperBound = q3 + (1.5*iqr)
    data=np.array(data)
    data = data[(data<=upperBound) & (data>=lowerBound)]
    return data

def getOutlierIndices(data):
    import numpy as np
    
    q1,q3 = np.percentile(sorted(data),[25,75])
    iqr = q3-q1
    lowerBound = q1 - (1.5*iqr)
    upperBound = q3 + (1.5*iqr)
    data=np.array(data)
    indices = np.argwhere((data<=upperBound) & (data>=lowerBound))
    return indices

def calculateGroupDifference(data1,data2,parametric=True,paired=False,discardOutliers=False,alternative='two-sided'):
    import numpy as np
    import scipy.stats as stt
    
    if(discardOutliers==True):
        data1 = removeOutliers(data1)
        data2 = removeOutliers(data2)
          
    mean = np.array([data1.mean(),data2.mean()])
    var = np.array([data1.var(),data2.var()])
    std = np.array([data1.std(),data2.std()])
    size = np.array([len(data1),len(data2)])
    
    if(var[0]==0 and var[1]==0):
        return 0,1
    
    if(parametric==True):
        if(paired==True):#Student's t test for repeated measures for normal distributions
            # calculate parametric paired t-test, with the assumption of distribution being normal
            statistic, pValue=stt.ttest_rel(data1,data2)
            #Calculate effect sie as explained in: http://www.real-statistics.com/students-t-distribution/paired-sample-t-test/cohens-d-paired-samples/
            r=stt.pearsonr(data1,data2)[0]
            s_z=np.sqrt(std[0]**2+std[1]**2-2*r*std[0]*std[1])
            s_rm=s_z/np.sqrt(2*(1-r))
            effectSize = (mean[0]-mean[1])/s_rm ##effect size for repeated measures
        elif(paired==False):#student's t test for independent variables having normal distribution
            # do F-test to see if the variances of two distributions are different
            if(var[1]!=0):
                F=var[0]/var[1]
                pVal=1-stt.f.cdf(F,len(data1)-1,len(data2)-1)#if, pVal<0.05, two distributions have different variance
            else:### if variance of one of the data is zero while the other is not, then consider this as the two dataset has different variance
                pVal=0
            if(pVal>0.05):
                statistic, pValue = stt.ttest_ind(data1,data2,equal_var=True)
            else:
                statistic, pValue = stt.ttest_ind(data1,data2,equal_var=False)
            
            #calculate effectSize using Cohen's D for t-test : https://en.wikipedia.org/wiki/Effect_size#Cohen's_d
            s_pooled=np.sqrt(((size[0]-1)*var[0]+(size[1]-1)*var[1])/float(size[0]+size[1]-2))
            effectSize = (mean[0]-mean[1])/s_pooled 
    elif(parametric==False):
        if(paired==True): #Wilcoxon Signed-rank test for repeated measures with non normal distribution
            # calculate non parametric t-test, when the data is not normally distributed
            statistic_W, pValue=stt.wilcoxon(data1,data2,alternative=alternative)
            
            # calculate effect size:  http://yatani.jp/teaching/doku.php?id=hcistats:wilcoxonsigned
            # effectSize = z / sqrt(totalSize)
            # z equals the sum of signed ranks divided by the square root of the sum of their squares. : https://stats.stackexchange.com/questions/306841/z-score-on-wilcoxon-signed-ranks-test
            # that is: z = w / sqrt(sum of squares of ranks)
            diff=data2-data1
            abs_diff=abs(diff)
            ranks=stt.rankdata(abs_diff)
            signs=[-1 if x<0 else 1 for x in diff]
            signed_rank=ranks*signs
            # the statistic is calculated as follows (gives the same result with the fisrt output of the stt.wilcoxon(data1,data2) function)
            #positiveRanks=signed_rank[signed_rank>0]
            #negativeRanks=-signed_rank[signed_rank<0]
            #w=min(np.sum(positiveRanks),np.sum(negativeRanks))
            z=np.sum(signed_rank)/np.sqrt(np.sum(signed_rank**2))
            
            effectSize = z/np.sqrt(size[0]+size[1]) # abs(r)	small=0.1	medium=0.3	large=0.5
        elif(paired==False):#Mann-Whitney U test
            statistic_U, pValue = stt.mannwhitneyu(data1,data2,alternative=alternative)
            
            #calculate effect size: http://yatani.jp/teaching/doku.php?id=hcistats:mannwhitney
            # effectSize = z / sqrt(totalSize)
            # z = (U - m_U) / std_U : https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test#Normal_approximation_and_tie_correction
            # where m_U = size1*size2/2 and std_U = sqrt(size1*size2*(size1+size2+1)/12.0)
            m_U = size[0]*size[1]/2.0
            std_U = np.sqrt(size[0]*size[1]*(size[0]+size[1]+1)/12.0)
            z = (statistic_U - m_U) / std_U
            
            effectSize = z / np.sqrt(size[0]+size[1]) # abs(r)	small=0.1	medium=0.3	large=0.5
        
    return effectSize,pValue

def checkDifferenceOfVariance(data1,data2,testType='F',discardOutliers=False):
    import scipy.stats as stt
    
    if(discardOutliers==True):
        data1 = removeOutliers(data1)
        data2 = removeOutliers(data2)
    
    if(testType=='F'):
        pValue = 1-stt.f.cdf(data1.var()/data2.var(),len(data1)-1,len(data2)-1)
        statistic = -1 # to indicate "don't care"
    elif(testType=='bartlett'):
        statistic, pValue = stt.bartlett(data1,data2)
    elif(testType=='levene'):
        statistic, pValue = stt.levene(data1,data2,center='mean')
        
    return statistic,pValue

def heatMap(matrix,displayPlotFlag,outputPath,backgroundColor,threshold,colormap='jet'):
    import matplotlib.pylab as plt
    import matplotlib as mpl
    
    cmap_=mpl.cm.get_cmap(colormap)
    cmap_.set_under(backgroundColor)
    
    plt.figure()
    plt.imshow(matrix, interpolation='none',vmin=threshold,cmap=cmap_)
    plt.colorbar()
    if(outputPath!=''):
        print("save to " + outputPath)
        plt.savefig(outputPath, transparent=True, dpi=300, bbox_inches='tight')
    
    #display the plot
    if displayPlotFlag:
        plt.show()

def drawCorrelationPlot(data1,data2,r,p,data1Label,data2Label,plotTitle,outputPath,pointNames=None,text=""):
    import numpy as np
    import matplotlib.pylab as plt
    import matplotlib as mpl
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.set_xlabel(data1Label,fontsize=18)
    ax.set_ylabel(data2Label,fontsize=18)
    ax.tick_params(axis='both',labelsize=10)
    mpl.rcParams['font.sans-serif'] = "Times New Roman"
    mpl.rcParams['font.family'] = "serif"
    if(text==""):
        text='r='+str("{0:.3f}".format(r))+'\np='+str("{0:.3f}".format(p))
    ax.text(0.79,0.9,text,horizontalalignment='left',verticalalignment='center',
            transform = ax.transAxes, color='grey',fontsize=12,
            bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})
    coeff=np.polyfit(data1,data2,1)
    data2Regressed=np.polyval(coeff,data1)
    plt.scatter(data1,data2,c='orchid',edgecolors='none',alpha=0.7)
    if pointNames!=None:
        for i in range(len(pointNames)):
            ax.annotate(pointNames[i],(data1[i],data2[i]),size=6)
    plt.plot(data1,data2Regressed,color='darkorchid',linewidth=2)
    plt.title(plotTitle)
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')
    return plt

def drawLongitudinalCorrelationPlot(data1,data2,r,p,data1Label,data2Label,plotTitle,outputPath,pointNames=None):
    import numpy as np
    import matplotlib.pylab as plt
    import matplotlib as mpl

    numTimepoints=len(data1[0])
    numSubjects=len(data1)
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.set_xlabel(data1Label)
    ax.set_ylabel(data2Label)
    data1Flat=data1.flatten()
    data2Flat=data2.flatten()
    coeff=np.polyfit(data1Flat,data2Flat,1)
    data2FlatRegressed=np.polyval(coeff,data1Flat)

    mpl.rcParams['font.sans-serif'] = "Times New Roman"
    mpl.rcParams['font.family'] = "serif"

#    ax.text(0.05,0.9, 'r='+str("{0:.3f}".format(r))+'\np='+("{0:.3f}".format(p)),
#            horizontalalignment='left',verticalalignment='center',
#            transform = ax.transAxes, color='grey',
#            bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})
    colors=['#2096BA','#FF7E5F','#613A43','#6C4F70','#849974']
    for i in range(numTimepoints):
        plt.scatter(data1[:,i],data2[:,i],c=colors[i],edgecolors='none',alpha=0.7)
    
    for i in range(numSubjects):
        if pointNames!=None:
            for j in range(numTimepoints):
                ax.annotate(pointNames[i]+"_"+str(j),(data1[i,j],data2[i,j]),size=6)
        clr=(np.random.rand(),np.random.rand(),np.random.rand())
        plt.plot(data1[i,:],data2[i,:],color=clr)
#    plt.plot(data1Flat,data2FlatRegressed,color='darkorchid',linewidth=2)
    plt.title(plotTitle)
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')
    plt.close()
    return plt

def drawCorrelationPlotWithConfidenceInterval(data1,data2,r,p,data1Label,data2Label,plotTitle,outputPath,pointNames=None,logScale=False):
    import matplotlib.pylab as plt
    import matplotlib as mpl
    import numpy as np
    import statsmodels.api as sm
    import scipy.stats as stt
    
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.set_xlabel(data1Label,fontsize=18)
    ax.set_ylabel(data2Label,fontsize=18)
    ax.tick_params(axis='both',labelsize=10)
    
    mpl.rcParams['font.sans-serif'] = "Times New Roman"
    mpl.rcParams['font.family'] = "serif"
    ax.text(0.84,0.87, 'r='+str("{0:.3f}".format(r))+'\np='+("{0:.3f}".format(p)),
            horizontalalignment='center',verticalalignment='center',fontsize=24,
            transform = ax.transAxes, color='grey',
            bbox={'facecolor':'white', 'alpha':0.7, 'pad':10})
    if(logScale):
        ax.set_yscale('log',basey=2)
    
    plt.scatter(data1,data2,c='orchid',alpha=0.7,edgecolors='none')
    if pointNames!=None:
        for i in range(len(pointNames)):
            ax.annotate(pointNames[i],(data1[i],data2[i]),size=6)
    
    ###OLS linear regression
    #http://markthegraph.blogspot.com/2015/05/using-python-statsmodels-for-ols-linear.html
    x=np.array(data1)
    y=np.array(data2)
    xMin=x.min()
    xMax=x.max()
    
    #regression line
    x = sm.add_constant(x)
    model = sm.OLS(y,x)
    fitted = model.fit()
    x_pred=np.linspace(xMin,xMax,50)
    x_pred2=sm.add_constant(x_pred)
    y_pred=fitted.predict(x_pred2)
    
    plt.plot(x_pred,y_pred,color='darkorchid',linewidth=2)
    
    #confidence interval for the regression
    y_hat = fitted.predict(x)
    y_err = y - y_hat
    mean_x = x.T[1].mean()
    n = len(x)
    dof = n - fitted.df_model - 1
    t = stt.t.ppf(1-0.025, df=dof)
    s_err = np.sum(np.power(y_err, 2))
    conf = t * np.sqrt((s_err/(n-2))*
                       (1.0/n + (np.power((x_pred-mean_x),2)/((np.sum(np.power(x_pred,2))) - n*(np.power(mean_x,2))))))
    upper = y_pred + abs(conf)
    lower = y_pred - abs(conf)
    #ax.fill_between(x_pred, lower, upper, color='#888888', alpha=0.4)
    
    #prediction interval
    from statsmodels.sandbox.regression.predstd import wls_prediction_std
    sdev, lower, upper = wls_prediction_std(fitted, exog=x_pred2, alpha=0.05)
    ax.fill_between(x_pred, lower, upper, color='#888888', alpha=0.1)
    
    plt.title(plotTitle)
    
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')

def drawViolinPlot(data,dataLabels,title,outputPath,xLabel="",yLabel="matching accuracy (%)",colors=['#2096BA','#351C4D', '#AB3E16','#849974', '#F7DFD4','#F5AB99'],rotation=0,yLim=[],scale=1.0): #shutter blue, nightfall, rust, fresh, macaron, tropical pink
    import matplotlib.pylab as plt
    import numpy as np
    
    numData=len(data)
    
    fig=plt.figure()
    
    ax=fig.add_subplot(111)
    ax.set_xlabel(xLabel,fontsize=16)
    ax.set_ylabel(yLabel,fontsize=16)
    ax.tick_params(axis='both',labelsize=10)
    if(len(yLim)==2):#use this line to set the y limits of the plot, useful for opening up space above the bars to put stars at postprocessing
        plt.ylim(yLim[0],yLim[1])
    #plt.yticks(range(size), size=7)
    
    plt.xlim(0,scale*(numData+1))
    positions=np.array(range(numData+1)[1:])*scale

    violin_parts=ax.violinplot(data, positions, points=60, widths=0.6, showmeans=True, showextrema=True, showmedians=False, bw_method='scott')
    for partname in ['cmins','cmaxes']:
        violin_parts[partname].set_edgecolor(colors)
        violin_parts[partname].set_linewidth(0.7)
    for partname in ['cmeans','cbars']:
        violin_parts[partname].set_edgecolor(colors)
        violin_parts[partname].set_linewidth(0.7)
    for i in range(len(violin_parts['bodies'])):
        violin_parts['bodies'][i].set_facecolor(colors[i])
        violin_parts['bodies'][i].set_edgecolor('none')
        violin_parts['bodies'][i].set_alpha(0.3)
        violin_parts['bodies'][i].set_linewidth(1)
    
    plt.xticks(positions, dataLabels, rotation=rotation)
    plt.title(title)
    
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')
    
def drawBoxPlot(data,dataLabels,title,outputPath,xLabel="",yLabel="matching accuracy (%)",colors=['#2096BA','#351C4D', '#AB3E16','#849974', '#F7DFD4','#F5AB99'],rotation=0,plotScatter=True,yLim=[],middleLine='mean'): #shutter blue, nightfall, rust, fresh, macaron, tropical pink
    import matplotlib.pylab as plt
    import numpy as np
    
    fig=plt.figure()
    
    ax=fig.add_subplot(111)
    if(xLabel!=""):
        ax.set_xlabel(xLabel,fontsize=16)
    if(yLabel!=""):
        ax.set_ylabel(yLabel,fontsize=16)
    ax.tick_params(axis='both',labelsize=10)
    if(len(yLim)==2):#use this line to set the y limits of the plot, useful for opening up space above the bars to put stars at postprocessing
        plt.ylim(yLim[0],yLim[1])
    #plt.yticks(range(size), size=7)

    boxprops = dict(linestyle='-', linewidth=4)
    if(plotScatter==False):
        markersize=4
    else:
        markersize=0
    flierprops = dict(marker='.', markerfacecolor='grey', markeredgecolor='none',markersize=markersize,linestyle='none') #outliers
    if(middleLine=='median'):
        medianprops = dict(linestyle='-', linewidth=1.5, color='firebrick') #median line
    else:
        medianprops = dict(linestyle='-', linewidth=0, color='firebrick') #median line
    
    if(middleLine=='mean'):
        meanlineprops = dict(linestyle='-', linewidth=1.5, color='firebrick') # mean line
    else:
        meanlineprops = dict(linestyle='-', linewidth=0, color='firebrick') # mean line
    meanpointprops = dict(marker='D', markeredgecolor='black', markerfacecolor='firebrick')#to put apoint to the mean instead of a line
    whiskerprops=dict(linestyle='--',linewidth=0.5,color='grey') # lines extending the boxes
    capprops=dict(linestyle='-',linewidth=0.5,color='grey') # caps perpendicular to whiskers
    boxplot_parts = ax.boxplot(data,whiskerprops=whiskerprops,boxprops=boxprops,capprops=capprops,medianprops=medianprops,meanprops=meanlineprops,meanline=True,showmeans=True,notch=False,flierprops=flierprops,patch_artist=True,zorder=0)
    for i in range(len(boxplot_parts['boxes'])):
        boxplot_parts['boxes'][i].set_edgecolor(colors[i])
        boxplot_parts['boxes'][i].set_facecolor('none')
        boxplot_parts['boxes'][i].set_linewidth(1.5)
    
    if(plotScatter==True):
        xScattered = []
        for i,dataChunk in enumerate(data):
            xScattered.append(np.random.normal(i+1,0.02,len(dataChunk)))
        for i in range(len(data)):
            plt.scatter(xScattered[i],data[i],color=colors[i],alpha=0.5,s=4,edgecolors='dimgray',linewidth=0.3,zorder=1)
        
    plt.xticks(range(len(dataLabels)+1)[1:], dataLabels, rotation=rotation)
    plt.title(title)
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')
    
def drawBarChart(objects,values,xLabel,yLabel,plotTitle,outputPath):
    import numpy as np
    import matplotlib.pylab as plt
    import matplotlib as mpl

    mpl.rcParams['font.sans-serif'] = "Times New Roman"
    mpl.rcParams['font.family'] = "serif"
    
    plt.figure()
    y_pos = np.arange(len(objects))
    plt.bar(y_pos,values, align='center',alpha=0.5)
    plt.xticks(y_pos,objects)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.title(plotTitle)
    plt.savefig(outputPath, transparent=True, dpi=300, bbox_inches='tight')
    plt.close()





def drawHistogram2Dataset(data1,data2,outputPath,score1,score2,scoreLabel1='',scoreLabel2='',data1Label='',data2Label='',plotTitle='',xLabel="matching accuracy (%)",yLabel="frequency",color1='dodgerblue',color2='magenta'):
    import numpy as np
    import scipy.stats as stt
    import matplotlib.pylab as plt
    import matplotlib as mpl
    
    mpl.rcParams['font.sans-serif'] = "Times New Roman"
    mpl.rcParams['font.family'] = "serif"
    
    fig=plt.figure()
    
    ax=fig.add_subplot(111)
    if(xLabel!=''):
        ax.set_xlabel(xLabel,fontsize=18)
    if(yLabel!=''):
        ax.set_ylabel(yLabel,fontsize=18)
    ax.tick_params(axis='both',labelsize=10)
    
    if(scoreLabel1!='' and scoreLabel2!=''):
        ax.text(0.74,0.89, str(scoreLabel1)+' : '+str("{0:.2f}".format(score1))+'\n'+ str(scoreLabel2)+' : '+("{0:.3f}".format(score2)),
            horizontalalignment='left',verticalalignment='center',
            transform = ax.transAxes, color='black',fontsize=18,
            bbox={'facecolor':'white', 'alpha':0.5, 'pad':8})
    
    
    
    pltData1=plt.hist(data1, bins=32, alpha=0.6,color=color1,edgecolor='none',label=data1Label,density=True)
    pltData2=plt.hist(data2, bins=32, alpha=0.5,color=color2,edgecolor='none',label=data2Label,density=True)

    #### plot normal curve fitting to histogram    
    xData1=np.linspace(data1.min(), data1.max(), 1000)
    xData2=np.linspace(data2.min(), data2.max(), 1000)

    meanData1, stdData1 = stt.norm.fit(data1)
    pdfData1 = stt.norm.pdf(xData1, meanData1, stdData1)
    
    meanData2, stdData2 = stt.norm.fit(data2)
    pdfData2 = stt.norm.pdf(xData2, meanData2, stdData2)
    
    ### normally, pdf will show the frequency of each bin (to plot the bins normalized, we added density=True to histogram function above). 
    ### If you would like to keep the y axis as actual numbers, you will need to scale the pdf by the area of the bins for each histogram.
    #scaleData1=len(data1)*(pltData1[1][1]-pltData1[1][0])
    #scaleData2=len(data2)*(pltData2[1][1]-pltData2[1][0])
    #plt.plot(xData1,pdfData1*scaleData1,'r-',color='dodgerblue')
    #plt.plot(xData2,pdfData2*scaleData2,'r-',color='magenta')
    plt.plot(xData1,pdfData1,'r-',color='dodgerblue',linewidth=2) 
    plt.plot(xData2,pdfData2,'r-',color='magenta',linewidth=2) 
    
    if(plotTitle!=''):
        plt.title(plotTitle)
    plt.legend(bbox_to_anchor=(0.2,1,0.6,0.1), loc="lower left",mode="expand",ncol=2,fancybox=True, framealpha=0.5,fontsize=12) #bbox_to_anchor=(x0,y0,width,height) bottomLeft of the screen is x,y=0,0
    
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')
    plt.close()
    

def drawHistogram(data,scores,scoreLabels,dataLabels,plotTitle,outputPath,xLabel="matching accuracy (%)",yLabel="frequency",colors=['#2096BA','#351C4D', '#AB3E16','#849974', '#F7DFD4','#F5AB99'],noBars=False,normalized=False): #shutter blue, nightfall, rust, fresh, macaron, tropical pink
    import numpy as np
    import scipy.stats as stt
    import matplotlib.pylab as plt
    import matplotlib as mpl
    
    mpl.rcParams['font.sans-serif'] = "Times New Roman"
    mpl.rcParams['font.family'] = "serif"
    
    numData=len(data)
    
    fig=plt.figure()
    
    ax=fig.add_subplot(111)
    ax.set_xlabel(xLabel,fontsize=18)
    ax.set_ylabel(yLabel,fontsize=18)
    ax.tick_params(axis='both',labelsize=10)
#    ax.text(0.74,0.89, str(scoreLabel1)+' : '+str("{0:.2f}".format(score1))+'\n'+ str(scoreLabel2)+' : '+("{0:.3f}".format(score2)),
#            horizontalalignment='left',verticalalignment='center',
#            transform = ax.transAxes, color='black',fontsize=18,
#            bbox={'facecolor':'white', 'alpha':0.5, 'pad':8})
    
    if(noBars==False):
        for i in range(numData):
            plt.hist(data[i], bins=10, alpha=0.6,color=colors[i],edgecolor='none',label=dataLabels[i],density=normalized)

    #### plot normal curve fitting to histogram   
    xData = []
    meanData = np.zeros(numData)
    stdData = np.zeros(numData)
    pdfData = []
    
    for i in range(numData):
        xData.append(np.linspace(data[i].min(), data[i].max(), 1000))
        meanData[i], stdData[i] = stt.norm.fit(data[i])
        pdfData.append(stt.norm.pdf(xData[i], meanData[i], stdData[i]))
    
    ### normally, pdf will show the frequency of each bin (to plot the bins normalized, we added density=True to histogram function above). 
    ### If you would like to keep the y axis as actual numbers, you will need to scale the pdf by the area of the bins for each histogram.
    for i in range(numData):
        #scaleData1=len(data[i])*(pltData1[1][1]-pltData1[1][0])
        if(noBars==False):
            plt.plot(xData[i],pdfData[i],'-',color=colors[i],linewidth=2) #plt.plot(xData1,pdfMale*scaleData1,'r-',color='dodgerblue')
        else:
            plt.plot(xData[i],pdfData[i],'-',color=colors[i],linewidth=2,label=dataLabels[i]) #plt.plot(xData1,pdfMale*scaleData1,'r-',color='dodgerblue')
    
    plt.title(plotTitle)
    plt.legend(bbox_to_anchor=(1.0,0.4,0.3,0.3), loc="lower left",mode="expand",ncol=1,fancybox=True, framealpha=0.5,fontsize=12) #bbox_to_anchor=(x0,y0,width,height) bottomLeft of the screen is x,y=0,0
    
    plt.savefig(outputPath, transparent=False, dpi=300, bbox_inches='tight')
    plt.close()


def drawHistogramSingleDataset(data,dataLabel,xLabel,yLabel,plotTitle,outputPath,color='dodgerblue'):
    import numpy as np
    import scipy.stats as stt
    import matplotlib.pylab as plt
    import matplotlib as mpl
    
    mpl.rcParams['font.sans-serif'] = "Times New Roman"
    mpl.rcParams['font.family'] = "serif"
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    
    plt.hist(data, bins=32, alpha=0.5,label=dataLabel)
    x=np.linspace(data.min(), data.max(), 1000)
    mean, std = stt.norm.fit(data)
    pdf= stt.norm.pdf(x, mean, std)
    ### normally, pdf will show the frequency of each bin (to plot the bins normalized, we added normed=True to histogram function above). 
    ### If you would like to keep the y axis as actual numbers, you will need to scale the pdf by the area of the bins for each histogram.
    #scale=len(diff)*(plt[1][1]-plt[1][0])
    plt.plot(x,pdf,'r-',color=color,linewidth=2) #plt.plot(x,pdf*scale,'r-',color='dodgerblue')
    
    plt.legend(loc='upper right', fancybox=True, framealpha=0.5)

    plt.title(plotTitle)
    plt.savefig(outputPath, transparent=True, dpi=300, bbox_inches='tight')
    plt.close()
