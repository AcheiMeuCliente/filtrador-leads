import React, { useState, useMemo, useRef, useEffect } from 'react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { ChevronUp, ChevronDown, ExternalLink, MapPin, Phone, Mail, MessageCircle, Eye, Globe, FileText, AlertCircle, Wand2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { Separator } from '@/components/ui/separator';
import { Empresa } from '@/types/empresa';
import EmpresaDetailsDialog from './EmpresaDetailsDialog';
import LeadAnalysisDialog from './LeadAnalysisDialog';
import NumeroVariacoes from './NumeroVariacoes';

interface EmpresasTableProps {
  empresas: Empresa[];
  isLoading?: boolean;
  onEndReached?: () => void;
}

type SortField = keyof Empresa;
type SortDirection = 'asc' | 'desc';

const EmpresasTable = ({ empresas, isLoading = false, onEndReached }: EmpresasTableProps) => {
  const [sortField, setSortField] = useState<SortField>('nome_principal');
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc');
  const [selectedEmpresa, setSelectedEmpresa] = useState<Empresa | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [analysisOpen, setAnalysisOpen] = useState(false);
  
  const parentRef = useRef<HTMLDivElement>(null);

  const sortedEmpresas = useMemo(() => {
    return [...empresas].sort((a, b) => {
      const aValue = a[sortField];
      const bValue = b[sortField];
      
      if (aValue === bValue) return 0;
      
      const comparison = aValue < bValue ? -1 : 1;
      return sortDirection === 'asc' ? comparison : -comparison;
    });
  }, [empresas, sortField, sortDirection]);

  const rowVirtualizer = useVirtualizer({
    count: sortedEmpresas.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80, // Estimated row height
    overscan: 5,
  });

  const virtualItems = rowVirtualizer.getVirtualItems();
  const totalSize = rowVirtualizer.getTotalSize();

  const paddingTop = virtualItems.length > 0 ? virtualItems[0].start : 0;
  const paddingBottom = virtualItems.length > 0
    ? totalSize - (virtualItems[virtualItems.length - 1].end)
    : 0;

  // Infinite scroll detection
  useEffect(() => {
    const [lastItem] = [...virtualItems].reverse();

    if (!lastItem) {
      return;
    }

    if (
      lastItem.index >= sortedEmpresas.length - 1 &&
      !isLoading &&
      onEndReached
    ) {
      onEndReached();
    }
  }, [virtualItems, sortedEmpresas.length, isLoading, onEndReached]);

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const SortableHeader = ({ field, children, isFirstColumn = false }: { field: SortField; children: React.ReactNode; isFirstColumn?: boolean }) => (
    <th 
      className={`px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-50 select-none bg-gray-50 ${
        isFirstColumn ? 'sticky left-0 z-20 border-r border-gray-200' : 'sticky top-0 z-10'
      }`}
      onClick={() => handleSort(field)}
    >
      <div className="flex items-center space-x-1">
        <span>{children}</span>
        {sortField === field && (
          sortDirection === 'asc' ? 
            <ChevronUp className="h-4 w-4" /> : 
            <ChevronDown className="h-4 w-4" />
        )}
      </div>
    </th>
  );

  const handleViewDetails = (empresa: Empresa) => {
    setSelectedEmpresa(empresa);
    setDetailsOpen(true);
  };

  const handleViewAnalysis = (empresa: Empresa) => {
    setSelectedEmpresa(empresa);
    setAnalysisOpen(true);
  };

  return (
    <TooltipProvider>
      <Card className="w-full flex flex-col h-[calc(100vh-200px)]">
        <CardHeader className="flex-none">
          <div className="flex items-center justify-between">
            <CardTitle className="text-xl flex items-center gap-2 text-blue-600 font-bold">
              <Eye className="h-6 w-6" />
              <span>Resultados</span>
            </CardTitle>
            <div className="text-sm text-gray-500">
              {empresas.length.toLocaleString()} empresa{empresas.length !== 1 ? 's' : ''} carregada{empresas.length !== 1 ? 's' : ''}
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="p-0 flex-1 overflow-hidden relative">
          <div 
            ref={parentRef} 
            className="h-full overflow-auto w-full"
          >
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50 sticky top-0 z-10 shadow-sm">
                <tr>
                  <SortableHeader field="nome_principal" isFirstColumn={true}>Empresa</SortableHeader>
                  <SortableHeader field="cnae_principal_nome">Atividade Principal (CNAE)</SortableHeader>
                  <SortableHeader field="porte">Enquadramento</SortableHeader>
                  <SortableHeader field="capital_social">Capital Social</SortableHeader>
                  <SortableHeader field="matriz_filial">Tipo</SortableHeader>
                  <SortableHeader field="inicio_atividade">Aberta há</SortableHeader>
                  <SortableHeader field="bairro">Bairro</SortableHeader>
                  <SortableHeader field="municipio">Município</SortableHeader>
                  <SortableHeader field="estado">UF</SortableHeader>
                  <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 sticky top-0 z-10">Mapa</th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider min-w-[160px] bg-gray-50 sticky top-0 z-10">
                    Telefone
                  </th>
                  <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 sticky top-0 z-10">WhatsApp</th>
                  <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 sticky top-0 z-10">Sugestões</th>
                  <th className="px-4 py-3 text-left text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 sticky top-0 z-10">Email</th>
                  <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 sticky top-0 z-10">
                    Pesquisar na Web
                  </th>
                  <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider leading-tight bg-gray-50 sticky top-0 z-10">
                    <div>Ver na</div>
                    <div>Receita Federal</div>
                  </th>
                  <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 sticky top-0 z-10">Detalhes</th>
                  <th className="px-4 py-3 text-center text-xs font-bold text-gray-500 uppercase tracking-wider bg-gray-50 sticky top-0 z-10">Análise</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {paddingTop > 0 && (
                  <tr>
                    <td style={{ height: `${paddingTop}px` }} colSpan={18} />
                  </tr>
                )}
                {virtualItems.map((virtualRow) => {
                  const empresa = sortedEmpresas[virtualRow.index];
                  return (
                    <tr 
                      key={empresa.cnpj} 
                      className="hover:bg-gray-50 transition-colors"
                      data-index={virtualRow.index}
                      ref={rowVirtualizer.measureElement}
                    >
                      {/* Empresa */}
                      <td className="px-4 py-4 text-sm text-gray-900 max-w-sm sticky left-0 bg-white z-10 border-r border-gray-100">
                        <div className="flex flex-col">
                          <div className="font-bold truncate" title={empresa.nome_principal}>{empresa.nome_principal}</div>
                          {empresa.nome_secundario && <div className="text-gray-600 text-xs truncate">{empresa.nome_secundario}</div>}
                          <div className="font-mono text-xs text-gray-500 mt-1">{empresa.cnpj}</div>
                        </div>
                      </td>
                      {/* Atividade Principal (CNAE) */}
                      <td className="px-4 py-4 text-sm text-gray-600 max-w-xs">
                        <div className="truncate" title={empresa.cnae_principal_nome}>
                          <div className="font-mono text-xs text-blue-600">{empresa.cnae_principal_codigo}</div>
                          <div className="truncate">{empresa.cnae_principal_nome}</div>
                        </div>
                      </td>
                      {/* Enquadramento */}
                      <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-600 max-w-xs">
                        <div className="font-medium">{empresa.porte}</div>
                        {empresa.descricao_natureza_juridica && <div className="text-xs text-gray-500 mt-1 truncate" title={empresa.descricao_natureza_juridica}>{empresa.descricao_natureza_juridica}</div>}
                        <div className="flex gap-1 flex-wrap mt-2">
                          {empresa.mei && <Badge variant="outline" className="text-xs bg-blue-50 text-blue-700 border-blue-200">MEI</Badge>}
                          {empresa.simples && <Badge variant="outline" className="text-xs bg-green-50 text-green-700 border-green-200">Simples</Badge>}
                        </div>
                      </td>
                      {/* Capital Social */}
                      <td className="px-4 py-4 whitespace-nowrap text-sm text-green-700 font-medium">{empresa.capital_social_formatado}</td>
                      {/* Tipo */}
                      <td className="px-4 py-4 whitespace-nowrap"><Badge variant="outline" className="text-xs">{empresa.matriz_filial_formatado}</Badge></td>
                      {/* Anos em Atividade */}
                      <td className="px-4 py-4 whitespace-nowrap text-sm text-center text-gray-600">{empresa.tempo_atividade_anos} anos</td>
                      {/* Bairro */}
                      <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-600">{empresa.bairro}</td>
                      {/* Município */}
                      <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-600">{empresa.municipio}</td>
                      {/* UF */}
                      <td className="px-4 py-4 whitespace-nowrap text-sm text-gray-600">{empresa.estado}</td>
                      {/* Mapa */}
                      <td className="px-4 py-4 whitespace-nowrap text-center">
                        {empresa.maps ? (
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button asChild variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-orange-50">
                                <a href={empresa.maps} target="_blank" rel="noopener noreferrer">
                                  <MapPin className="h-4 w-4 text-orange-600" />
                                </a>
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent><p>{empresa.endereco_completo || 'Ver no mapa'}</p></TooltipContent>
                          </Tooltip>
                        ) : (
                          <span className="text-gray-400 text-sm">—</span>
                        )}
                      </td>
                      {/* Telefone */}
                      <td className="px-4 py-3 text-sm text-gray-600 align-top min-w-[160px]">
                        <div className="flex flex-col gap-y-2">
                          {(empresa.contatos || []).length > 0 ? (
                            (empresa.contatos || []).map((contato, index) => (
                              <div key={index} className="min-h-[2.5rem] flex items-center gap-2">
                                <div className="flex items-center gap-2 text-slate-700">
                                  <Tooltip>
                                    <TooltipTrigger asChild>
                                      <a href={contato.tel_link || '#'} className="text-slate-600 hover:text-slate-800 transition-colors">
                                        <Phone className="h-4 w-4 flex-shrink-0" />
                                      </a>
                                    </TooltipTrigger>
                                    <TooltipContent><p>Ligar para este número</p></TooltipContent>
                                  </Tooltip>
                                  <span>{contato.numero}</span>
                                </div>
                                <div className="flex items-center ml-auto">
                                  <Tooltip>
                                    <TooltipTrigger asChild>
                                      <div className="cursor-help ml-2">
                                        <AlertCircle className="h-4 w-4 text-amber-500" />
                                      </div>
                                    </TooltipTrigger>
                                    <TooltipContent side="right" className="max-w-[320px] p-3">
                                      <div className="space-y-3 text-xs text-slate-700">
                                        <div>
                                          <p className="font-semibold text-amber-800">Importante:</p>
                                          <p className="mt-1">Alguns números podem funcionar no WhatsApp mas não para ligações convencionais devido a:</p>
                                          <ul className="mt-1.5 space-y-1 pl-4 list-disc text-slate-600">
                                            <li>Falta do 9º dígito em celulares de cadastros antigos.</li>
                                            <li>Números de telefone fixo informados como celular.</li>
                                            <li>Formato não compatível com as regras da Anatel.</li>
                                          </ul>
                                        </div>
                                        <Separator />
                                        <div>
                                          <p className="font-semibold text-emerald-800">Recomendação:</p>
                                          <p className="mt-1">Use a varinha mágica <Wand2 className="inline-block h-3.5 w-3.5 text-purple-600" /> para ver sugestões de formato caso o contato principal não funcione.</p>
                                        </div>
                                      </div>
                                    </TooltipContent>
                                  </Tooltip>
                                </div>
                              </div>
                            ))
                          ) : (
                            <span className="text-gray-400">Não informado</span>
                          )}
                        </div>
                      </td>
                      {/* WhatsApp */}
                      <td className="px-4 py-3 text-sm text-center align-top">
                        <div className="flex flex-col items-center justify-center gap-y-2">
                          {(empresa.contatos || []).map((contato, index) => (
                            <div key={index} className="min-h-[2.5rem] flex items-center justify-center">
                              {contato.whatsapp_link ? (
                                <Tooltip>
                                  <TooltipTrigger asChild>
                                    <a href={contato.whatsapp_link} target="_blank" rel="noopener noreferrer"><MessageCircle className="h-4 w-4 text-green-600" /></a>
                                  </TooltipTrigger>
                                  <TooltipContent><p>WhatsApp</p></TooltipContent>
                                </Tooltip>
                              ) : <div className="w-4" /> /* Espaçamento para alinhar */}
                            </div>
                          ))}
                        </div>
                      </td>
                      {/* Sugestões */}
                      <td className="px-4 py-3 text-sm text-center align-top">
                        <div className="flex flex-col items-center justify-center gap-y-2">
                          {(empresa.contatos || []).map((contato, index) => (
                            <div key={index} className="min-h-[2.5rem] flex items-center justify-center">
                              <NumeroVariacoes telefone={contato.numero} />
                            </div>
                          ))}
                        </div>
                      </td>
                      {/* Email */}
                      <td className="px-4 py-4 whitespace-nowrap text-sm text-blue-600 max-w-xs">
                        {empresa.email ? (<a href={`mailto:${empresa.email}`} className="hover:underline truncate">{empresa.email}</a>) : (<span className="text-gray-400 text-sm">—</span>)}
                      </td>
                      {/* Site */}
                      <td className="px-4 py-4 whitespace-nowrap text-center">
                        {empresa.site ? (<Tooltip><TooltipTrigger asChild><Button asChild variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-purple-50"><a href={empresa.site} target="_blank" rel="noopener noreferrer"><Globe className="h-4 w-4 text-purple-600" /></a></Button></TooltipTrigger><TooltipContent><p>Pesquisar na web</p></TooltipContent></Tooltip>) : (<span className="text-gray-400 text-sm">—</span>)}
                      </td>
                      {/* Consulta Online */}
                      <td className="px-4 py-4 whitespace-nowrap text-center">
                        {empresa.receita_federal ? (<Tooltip><TooltipTrigger asChild><Button asChild variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-gray-100"><a href={empresa.receita_federal} target="_blank" rel="noopener noreferrer"><ExternalLink className="h-4 w-4 text-gray-600" /></a></Button></TooltipTrigger><TooltipContent><p>Ver na Receita Federal</p></TooltipContent></Tooltip>) : (<span className="text-gray-400 text-sm">—</span>)}
                      </td>
                      {/* Detalhes */}
                      <td className="px-4 py-4 whitespace-nowrap text-center">
                        <Tooltip><TooltipTrigger asChild><Button variant="ghost" size="sm" className="h-8 w-8 p-0 hover:bg-indigo-50" onClick={() => handleViewDetails(empresa)}><Eye className="h-4 w-4 text-indigo-600" /></Button></TooltipTrigger><TooltipContent><p>Ver detalhes completos</p></TooltipContent></Tooltip>
                      </td>
                      {/* Análise */}
                      <td className="px-2 py-2 whitespace-nowrap text-center">
                          <Tooltip>
                            <TooltipTrigger asChild>
                              <Button 
                              variant="secondary" 
                                size="sm" 
                              className="h-8 w-8 p-0 rounded-full bg-blue-50 hover:bg-blue-100"
                              onClick={() => handleViewAnalysis(empresa)}
                              >
                              <FileText className="h-4 w-4 text-blue-700" />
                              <span className="sr-only">Análise de Lead</span>
                              </Button>
                            </TooltipTrigger>
                            <TooltipContent>
                            <p>Raio-X Completo do Lead</p>
                            </TooltipContent>
                          </Tooltip>
                      </td>
                    </tr>
                  );
                })}
                {paddingBottom > 0 && (
                  <tr>
                    <td style={{ height: `${paddingBottom}px` }} colSpan={18} />
                  </tr>
                )}
              </tbody>
            </table>
            {isLoading && (
              <div className="py-4 text-center text-sm text-gray-500">
                Carregando mais empresas...
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      <EmpresaDetailsDialog 
        empresa={selectedEmpresa}
        open={detailsOpen}
        onOpenChange={setDetailsOpen}
      />
      
      <LeadAnalysisDialog 
        empresa={selectedEmpresa}
        isOpen={analysisOpen}
        onClose={() => setAnalysisOpen(false)}
      />
    </TooltipProvider>
  );
};

export default EmpresasTable;
