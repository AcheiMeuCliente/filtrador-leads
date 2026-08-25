import React from 'react';
import { 
  Phone, Mail, MessageCircle, MapPin, Globe, ExternalLink, MoreVertical, Eye, 
  Search, FileText, TrendingUp, Instagram, AlertCircle, Wand2
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardFooter } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { Tooltip, TooltipProvider, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { Empresa } from '@/types/empresa';
import NumeroVariacoes from './NumeroVariacoes';

interface EmpresaCardProps {
  empresa: Empresa;
  onViewDetails: (empresa: Empresa) => void;
  onViewAnalysis: (empresa: Empresa) => void;
}

const EmpresaCard: React.FC<EmpresaCardProps> = ({ empresa, onViewDetails, onViewAnalysis }) => {
  
  const getSituacaoBadge = (situacao: string, variant: Empresa['situacao_variant']) => {
    const variants = {
      success: "bg-green-100 text-green-800 border-green-200",
      warning: "bg-yellow-100 text-yellow-800 border-yellow-200",
      destructive: "bg-red-100 text-red-800 border-red-200",
      default: "outline"
    };
    return <Badge variant={variant === 'default' ? 'outline' : 'default'} className={variants[variant]}>{situacao}</Badge>;
  };

  return (
    <TooltipProvider>
      <Card className="flex flex-col h-full bg-gradient-to-b from-white to-slate-50/80 backdrop-blur-sm border border-slate-200/80 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group">
        <CardHeader className="flex flex-row items-start justify-between p-4 bg-white border-b border-slate-100">
          <div className="flex flex-wrap gap-2">
            {getSituacaoBadge(empresa.situacao, empresa.situacao_variant)}
            {empresa.mei && <Badge variant="outline" className="border-blue-300 text-blue-800">MEI</Badge>}
            {empresa.simples && <Badge variant="outline" className="border-purple-300 text-purple-800">Simples</Badge>}
            <Badge variant="outline">{empresa.matriz_filial_formatado}</Badge>
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8"><MoreVertical className="h-4 w-4" /></Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => onViewDetails(empresa)}><Eye className="mr-2 h-4 w-4" />Ver Detalhes</DropdownMenuItem>
              <DropdownMenuItem onClick={() => onViewAnalysis(empresa)}><FileText className="mr-2 h-4 w-4" />Análise de Lead</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </CardHeader>

        <CardContent className="flex-grow p-4 pt-0">
          <div className="mt-4 p-3 bg-white rounded-lg border border-slate-100">
            <h3 className="font-semibold text-base text-slate-900 truncate" title={empresa.nome_principal}>{empresa.nome_principal}</h3>
            {empresa.nome_secundario && <p className="text-sm text-slate-500 truncate" title={empresa.nome_secundario}>{empresa.nome_secundario}</p>}
            <div className="flex items-center gap-2 mt-1">
              <p className="font-mono text-xs text-slate-500">{empresa.cnpj}</p>
              {empresa.receita_federal && (
                <Tooltip>
                  <TooltipTrigger asChild>
                    <a href={empresa.receita_federal} target="_blank" rel="noopener noreferrer" aria-label="Consultar na Receita Federal">
                      <Badge variant="outline" className="cursor-pointer bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border-indigo-200 transition-colors flex items-center gap-1">
                        <ExternalLink className="h-3 w-3" /> Consultar RF
                      </Badge>
                    </a>
                  </TooltipTrigger>
                  <TooltipContent><p>Consultar na Receita Federal</p></TooltipContent>
                </Tooltip>
              )}
            </div>
            <div className="mt-2">
              <Badge variant="outline" className="font-normal text-blue-900 bg-blue-100 border-blue-200 shadow-sm">{empresa.cnae_principal_codigo} - {empresa.cnae_principal_nome}</Badge>
            </div>
            <div className="mt-2">
              <Badge variant="outline" className="font-normal text-purple-900 bg-purple-50 border-purple-200">{empresa.descricao_natureza_juridica}</Badge>
            </div>
          </div>
          
          <Separator className="my-4 opacity-30" />

          <div className="mt-4 p-3 bg-emerald-50/50 rounded-lg border border-emerald-100/50">
            <h4 className="flex items-center text-xs font-semibold text-emerald-800 mb-2 uppercase tracking-wider"><TrendingUp className="h-4 w-4 mr-2 text-emerald-600" />Visão Geral</h4>
            <p className="text-xs text-emerald-900 leading-relaxed">{empresa.resumo_executivo}</p>
          </div>

          {(empresa.cnaes_secundarios || []).length > 0 && (
            <div className="mt-4 p-3 bg-slate-50/80 rounded-lg border border-slate-100">
              <h4 className="flex items-center text-xs font-semibold text-slate-700 mb-2 uppercase tracking-wider">Outras Atividades</h4>
              <div className="flex flex-wrap gap-2">
                {empresa.cnaes_secundarios.map((cnae) => (
                  <Badge key={cnae.code} variant="outline" className="font-normal text-slate-700 bg-white/80 border-slate-200">{cnae.code} - {cnae.name}</Badge>
                ))}
              </div>
            </div>
          )}

          <Separator className="my-4 opacity-30" />
          
          <div className="mt-4 p-3 bg-blue-50/50 rounded-lg border border-blue-100/50">
            <div className="flex items-center justify-between mb-2">
              <h4 className="text-xs font-semibold text-slate-700 uppercase tracking-wider">Contatos</h4>
              <Tooltip>
                <TooltipTrigger asChild>
                  <div className="cursor-help">
                    <AlertCircle className="h-4 w-4 text-amber-500" />
                  </div>
                </TooltipTrigger>
                <TooltipContent side="left" className="max-w-[320px] p-3">
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
            <div className="space-y-3 text-sm">
              {(empresa.contatos || []).map((contato, i) => (
                <div key={`phone-${i}`} className="flex items-center gap-2">
                  <div className="flex items-center gap-2 text-slate-700">
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <a href={contato.tel_link || '#'} className="text-slate-600 hover:text-slate-800 transition-colors"><Phone className="h-4 w-4 flex-shrink-0" /></a>
                      </TooltipTrigger>
                      <TooltipContent><p>Ligar para este número</p></TooltipContent>
                    </Tooltip>
                    <span>{contato.numero}</span>
                  </div>
                  <div className="flex items-center ml-auto">
                    {contato.whatsapp_link && (
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <a href={contato.whatsapp_link} target="_blank" rel="noopener noreferrer" className="text-emerald-600 hover:text-emerald-700"><MessageCircle className="h-4 w-4" /></a>
                        </TooltipTrigger>
                        <TooltipContent><p>Abrir no WhatsApp</p></TooltipContent>
                      </Tooltip>
                    )}
                    <NumeroVariacoes telefone={contato.numero} />
                  </div>
                </div>
              ))}
              {empresa.email && (
                <div className="flex items-center gap-3 text-slate-700">
                  <Mail className="h-4 w-4 text-indigo-600 flex-shrink-0" />
                  <a href={`mailto:${empresa.email}`} className="truncate hover:underline text-indigo-600 hover:text-indigo-700" title={empresa.email}>{empresa.email}</a>
                </div>
              )}
              
              {empresa.site && (
                <div className="flex items-start gap-3">
                  <a href={empresa.site} target="_blank" rel="noopener noreferrer" className="flex items-start gap-3 group/web">
                    <Globe className="h-4 w-4 text-violet-600 flex-shrink-0 mt-0.5" />
                    <p className="text-violet-600 group-hover/web:underline truncate" title={empresa.site}>
                      {empresa.site.replace(/^(https?:\/\/)?(www\.)?/, '').split('/')[0]}
                    </p>
                  </a>
                </div>
              )}
              <div className="flex items-start gap-3">
                <a href={`https://www.google.com/search?q=${encodeURIComponent(empresa.nome_principal + ' sao paulo sp instagram')}`} target="_blank" rel="noopener noreferrer" className="flex items-start gap-3 group/instagram">
                  <Instagram className="h-4 w-4 text-pink-600 flex-shrink-0 mt-0.5" />
                  <p className="text-slate-600 group-hover/instagram:text-pink-600 group-hover/instagram:underline transition-colors">Procurar no Instagram</p>
                </a>
              </div>
              <div className="flex items-start gap-3">
                <a href={`https://www.google.com/search?q=${encodeURIComponent(empresa.nome_principal + ' sao paulo sp')}`} target="_blank" rel="noopener noreferrer" className="flex items-start gap-3 group/web">
                  <Search className="h-4 w-4 text-slate-500 flex-shrink-0 mt-0.5" />
                  <p className="text-slate-600 group-hover/web:underline">Pesquisar na Web</p>
                </a>
              </div>
              <div className="flex items-start gap-3">
                <a href={empresa.maps || '#'} target="_blank" rel="noopener noreferrer" className="flex items-start gap-3 group/map">
                  <MapPin className="h-4 w-4 text-rose-600 flex-shrink-0 mt-0.5" />
                  <p className="capitalize text-slate-700 line-clamp-2 group-hover/map:underline" title={empresa.endereco_completo}>
                    {empresa.endereco_completo?.toLowerCase()}
                  </p>
                </a>
              </div>
            </div>
          </div>
          <Separator className="my-4 opacity-30" />
          <div className="grid grid-cols-2 gap-2 text-center">
            <div className="p-2 rounded-md bg-slate-50/70">
              <div className="text-xs text-slate-500">Capital Social</div>
              <div className="font-semibold text-sm text-green-800">{empresa.capital_social_formatado}</div>
            </div>
            <div className="p-2 rounded-md bg-slate-50/70">
              <div className="text-xs text-slate-500">Porte</div>
              <div className="font-semibold text-sm text-slate-800">{empresa.porte_formatado}</div>
            </div>
            <div className="p-2 rounded-md bg-slate-50/70">
              <div className="text-xs text-slate-500">Início Atividade</div>
              <div className="font-semibold text-sm text-slate-800">{empresa.inicio_atividade_formatado}</div>
            </div>
            <div className="p-2 rounded-md bg-slate-50/70">
              <div className="text-xs text-slate-500">Tempo Atividade</div>
              <div className="font-semibold text-sm text-slate-800">{empresa.tempo_atividade_anos} anos</div>
            </div>
          </div>
        </CardContent>
        <CardFooter className="p-4 bg-slate-50/80 border-t mt-auto">
          <div className="flex w-full items-center gap-2">
            <Button size="sm" onClick={() => onViewDetails(empresa)} className="flex-1">
              <Eye className="mr-2 h-4 w-4" />
              Detalhes
            </Button>
            <Button size="sm" variant="outline" onClick={() => onViewAnalysis(empresa)} className="flex-1">
              <FileText className="mr-2 h-4 w-4" />
              Análise
            </Button>
          </div>
        </CardFooter>
      </Card>
    </TooltipProvider>
  );
};

export default React.memo(EmpresaCard); 