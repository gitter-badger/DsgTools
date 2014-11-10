<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'><qgis version="2.6.0-Brighton" minimumScale="1" maximumScale="1" simplifyDrawingHints="0" minLabelScale="0" maxLabelScale="1e+08" simplifyDrawingTol="1" simplifyMaxScale="1" hasScaleBasedVisibilityFlag="0" simplifyLocal="1" scaleBasedLabelVisibilityFlag="0">
  <edittypes>
    <edittype widgetv2type="TextEdit" name="OGC_FID">
      <widgetv2config IsMultiline="0" fieldEditable="0" UseHtml="0" labelOnTop="0"/>
    </edittype>
    <edittype widgetv2type="ValueMap" name="tiporef">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Altimétrico" value="1"/>
        <value key="Planimétrico" value="2"/>
        <value key="Planialtimétrico" value="3"/>
        <value key="Gravimétrico" value="4"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="geometriaaproximada">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Sim" value="1"/>
        <value key="Não" value="2"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="proximidade">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Desconhecida" value="0"/>
        <value key="Isolado" value="14"/>
        <value key="Adjacente" value="15"/>
        <value key="Coincidente" value="16"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="rede">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Desconhecida" value="0"/>
        <value key="Estadual" value="2"/>
        <value key="Municipal" value="3"/>
        <value key="Nacional" value="14"/>
        <value key="Privada" value="15"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="sistemageodesico">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="SAD-69" value="1"/>
        <value key="SIRGAS" value="2"/>
        <value key="WGS-84" value="3"/>
        <value key="Córrego Alegre" value="4"/>
        <value key="Astro Chuá" value="5"/>
        <value key="Outra referência" value="6"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="referencialaltim">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Torres" value="1"/>
        <value key="Imbituba" value="2"/>
        <value key="Santana" value="3"/>
        <value key="Local" value="4"/>
        <value key="Outra referência" value="5"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="referencialgrav">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Desconhecido" value="0"/>
        <value key="Postdam 1930" value="1"/>
        <value key="IGSN71" value="2"/>
        <value key="Absoluto" value="3"/>
        <value key="Local" value="4"/>
        <value key="Não Aplicável" value="97"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="situacaomarco">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Bom" value="1"/>
        <value key="Destruído" value="2"/>
        <value key="Destruído sem chapa" value="3"/>
        <value key="Destruído com chapa danificada" value="4"/>
        <value key="Não encontrado" value="5"/>
        <value key="Não visitado" value="6"/>
        <value key="Não construído" value="7"/>
        <value key="Desconhecido" value="0"/>
      </widgetv2config>
    </edittype>    <edittype widgetv2type="ValueMap" name="tipoptorefgeodtopo">
      <widgetv2config fieldEditable="1" labelOnTop="0">
        <value key="Desconhecido" value="0"/>
        <value key="Vértice de Triangulação - VT" value="1"/>
        <value key="Referência de Nível - RN" value="2"/>
        <value key="Estação Gravimétrica - EG" value="3"/>
        <value key="Estação de Poligonal - EP" value="4"/>
        <value key="Ponto Astronômico - PA" value="5"/>
        <value key="Ponto barométrico - B" value="6"/>
        <value key="Ponto Trigonométrico - RV" value="7"/>
        <value key="Ponto de Satélite - SAT" value="8"/>
        <value key="Outros" value="99"/>
      </widgetv2config>
    </edittype>  </edittypes>
</qgis>