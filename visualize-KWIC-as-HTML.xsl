<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:template match="/">
        <html>
            <head>
                <title>Testing Decknamen</title>
            </head>
            <body>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match ="KWIC">
        <hr/>
        <div>
        <xsl:value-of select="@n"/><xsl:text>, ID/ana: </xsl:text><xsl:value-of select="@ana"/>
            <xsl:apply-templates/>
        </div>
    </xsl:template>
    
    <xsl:template match="TEXT">
        <hr/>
        <p>Number of terms in KWIC: <xsl:value-of select="count(child::term)"/></p>
        <hr/><xsl:text>START-TEXT
        
        </xsl:text>
        <xsl:value-of select="@xml:id"/>
        <xsl:apply-templates/>
    </xsl:template>
    
    <xsl:template match ="head">
        <h3><xsl:apply-templates/></h3>
    </xsl:template>
    
    <xsl:template match ="term">
        <span style="background-color:coral;">
            <xsl:apply-templates/></span>
    </xsl:template>
    
    <xsl:template match ="lb">
        <br/>
    </xsl:template>
    
</xsl:stylesheet>