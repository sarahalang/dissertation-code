<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    version="2.0">

    <xsl:template match="/">
        <xsl:variable name="root" select="/"/>

        <result>
            <xsl:for-each select="//term">
                <KWIC>
                    <xsl:attribute name="n">
                        <xsl:value-of select="normalize-space(.)"/>
                    </xsl:attribute>
                    <xsl:attribute name="xml:id"><xsl:value-of select="@xml:id"/></xsl:attribute>

                    <!-- check how many preceding and following siblings there are -->
                    <xsl:variable name="numberOfPrecedings" select="count(current()/preceding::term)"/>
                    <xsl:variable name="numberOfFollowings" select="count(current()/following::term)"/>
                    <!-- create an attribute to mark incomplete/short KWICs -->
                    <xsl:if test="(5 > $numberOfPrecedings) or (5 > $numberOfFollowings)">
                        <xsl:attribute name="ana">incomplete-kwic</xsl:attribute>
                    </xsl:if>
                    <!-- determine the number of preceding siblings:
                        if value >= 5, take 5, if not, take the corresponding number -->
                    <xsl:variable name="kwickstartposition">
                        <xsl:choose>
                            <xsl:when test="$numberOfPrecedings >= 5">
                                <xsl:value-of select="5"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$numberOfPrecedings"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>

                    <xsl:variable name="kwickendposition">
                        <xsl:choose>

                            <xsl:when test="$numberOfFollowings >= 5">
                                <xsl:value-of select="5"/>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:value-of select="$numberOfFollowings"/>
                            </xsl:otherwise>
                        </xsl:choose>
                    </xsl:variable>

                    <debugOutput>
                        <xsl:text> variable test:
                values before </xsl:text>
                        <xsl:value-of select="$kwickstartposition"/>
                        <xsl:text>
                , values after </xsl:text>
                        <xsl:value-of select="$kwickendposition"/>
                        <xsl:text> -- </xsl:text>
                        <xsl:value-of select="current()/preceding::term[xs:integer($kwickstartposition)]"/>
                        <xsl:value-of select="current()/preceding::term[xs:integer($kwickendposition)]"/>
                        <xsl:text>


                </xsl:text>
                    </debugOutput>

                    <!-- get the starting node for the KWIC relevant to currently processed item -->
                    <xsl:variable name="kwicstart" select="current()/preceding::term[xs:integer($kwickstartposition)]"/>
                    <xsl:variable name="kwicend" select="current()/following::term[xs:integer($kwickendposition)]"/>

                    <TEXT>
                        <!-- the start and end nodes are set manually using copy-of
                             since intersect excludes those. This allowed for a cleaner solution. -->
                        <xsl:copy-of select="$kwicstart"></xsl:copy-of>
                        
                        <xsl:copy-of select="( $root/$kwicstart/following-sibling::* | $root/$kwicstart/following-sibling::text() )
                            intersect
                            ( $root/$kwicend/preceding-sibling::* |  $root/$kwicend/preceding-sibling::text() )"></xsl:copy-of>
                        <xsl:copy-of select="$kwicend"></xsl:copy-of>
                        <!-- | $root/$kwicstart/following-sibling::node()|
                        $root/$kwicstart/following-sibling::node() |-->
                    </TEXT>
                    <result/>
                    <log/>

                </KWIC>
            </xsl:for-each>

        </result>

    </xsl:template>
</xsl:stylesheet>
