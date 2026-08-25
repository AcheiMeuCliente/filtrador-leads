
import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { 
  Building2, 
  MapPin, 
  Phone, 
  Mail, 
  Globe, 
  Calendar, 
  DollarSign,
  ExternalLink,
  FileText,
  User,
  Hash
} from 'lucide-react';
import { Empresa } from '@/types/empresa';

interface EmpresaDetailsDialogProps {
  empresa: Empresa | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const EmpresaDetailsDialog = ({ empresa, open, onOpenChange }: EmpresaDetailsDialogProps) => {
  if (!empresa) return null;

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(value);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getSituacaoColor = (situacao: string) => {
    switch (situacao.toLowerCase()) {
      case 'ativa': return 'bg-green-100 text-green-800 border-green-200';
      case 'suspensa': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'baixada': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto" aria-describedby="empresa-details-description">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2 text-xl">
            <Building2 className="h-6 w-6" />
            {empresa.nome_fantasia || empresa.razao_social}
          </DialogTitle>
          <div id="empresa-details-description" className="sr-only">
            Detalhes completos da empresa incluindo informações de contato, endereço, atividade econômica e dados financeiros
          </div>
        </DialogHeader>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Informações Básicas */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Hash className="h-5 w-5" />
                Identificação
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium text-gray-600">CNPJ</label>
                <p className="font-mono text-lg">{empresa.cnpj}</p>
              </div>
              
              <div>
                <label className="text-sm font-medium text-gray-600">Razão Social</label>
                <p className="font-medium">{empresa.razao_social}</p>
              </div>
              
              {empresa.nome_fantasia && (
                <div>
                  <label className="text-sm font-medium text-gray-600">Nome Fantasia</label>
                  <p>{empresa.nome_fantasia}</p>
                </div>
              )}
              
              <div>
                <label className="text-sm font-medium text-gray-600">Situação</label>
                <div className="mt-1">
                  <Badge className={getSituacaoColor(empresa.situacao)}>
                    {empresa.situacao}
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Contato */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Phone className="h-5 w-5" />
                Contato
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {empresa.email && (
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-600">Email</label>
                    <p>{empresa.email}</p>
                  </div>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => window.open(`mailto:${empresa.email}`, '_blank')}
                  >
                    <Mail className="h-4 w-4" />
                  </Button>
                </div>
              )}
              
              {empresa.telefones && (
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-600">Telefone</label>
                    <p>{empresa.telefones}</p>
                  </div>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => window.open(`tel:${empresa.telefones}`, '_blank')}
                  >
                    <Phone className="h-4 w-4" />
                  </Button>
                </div>
              )}
              
              {empresa.whatsapp_1 && (
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-600">WhatsApp</label>
                    <p>Disponível</p>
                  </div>
                  <Button 
                    variant="outline" 
                    size="sm"
                    className="text-green-600 border-green-200 hover:bg-green-50"
                    onClick={() => window.open(empresa.whatsapp_1, '_blank')}
                  >
                    <Phone className="h-4 w-4" />
                  </Button>
                </div>
              )}
              
              {empresa.site && (
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-600">Website</label>
                    <p className="truncate">{empresa.site}</p>
                  </div>
                  <Button 
                    variant="outline" 
                    size="sm"
                    onClick={() => window.open(empresa.site, '_blank')}
                  >
                    <Globe className="h-4 w-4" />
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Endereço */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <MapPin className="h-5 w-5" />
                Endereço
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <p>{empresa.logradouro}, {empresa.numero}</p>
              {empresa.complemento && <p>{empresa.complemento}</p>}
              <p>{empresa.bairro}</p>
              <p>{empresa.municipio} - {empresa.estado}</p>
              <p>CEP: {empresa.cep}</p>
              
              <div className="pt-2">
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => window.open(empresa.maps, '_blank')}
                  className="w-full"
                >
                  <MapPin className="h-4 w-4 mr-2" />
                  Ver no Mapa
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Atividade Econômica */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <FileText className="h-5 w-5" />
                Atividade Econômica
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-600">CNAE Principal</label>
                <p className="text-sm font-mono text-gray-500">{empresa.cnae_principal_codigo}</p>
                <p className="text-sm">{empresa.cnae_principal_nome}</p>
              </div>
              
              <div>
                <label className="text-sm font-medium text-gray-600">Porte</label>
                <p>{empresa.porte}</p>
              </div>
              
              <div>
                <label className="text-sm font-medium text-gray-600">Natureza Jurídica</label>
                <p className="text-sm">{empresa.descricao_natureza_juridica}</p>
              </div>
            </CardContent>
          </Card>

          {/* Informações Financeiras */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <DollarSign className="h-5 w-5" />
                Informações Financeiras
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-600">Capital Social</label>
                <p className="text-lg font-semibold">{formatCurrency(empresa.capital_social)}</p>
              </div>
              
              <div className="flex gap-2">
                {empresa.mei && (
                  <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
                    MEI
                  </Badge>
                )}
                {empresa.simples && (
                  <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                    Simples Nacional
                  </Badge>
                )}
                <Badge variant="outline">
                  {empresa.matriz_filial}
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Datas Importantes */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2 text-lg">
                <Calendar className="h-5 w-5" />
                Datas Importantes
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-600">Início da Atividade</label>
                <p>{formatDate(empresa.inicio_atividade)}</p>
              </div>
              
              <div>
                <label className="text-sm font-medium text-gray-600">Última Atualização</label>
                <p>{formatDate(empresa.atualizacao_cadastral)}</p>
              </div>
              
              {empresa.data_opcao_simples && (
                <div>
                  <label className="text-sm font-medium text-gray-600">Opção Simples Nacional</label>
                  <p>{formatDate(empresa.data_opcao_simples)}</p>
                </div>
              )}
              
              {empresa.data_opcao_mei && (
                <div>
                  <label className="text-sm font-medium text-gray-600">Opção MEI</label>
                  <p>{formatDate(empresa.data_opcao_mei)}</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        <Separator className="my-4" />

        <div className="flex justify-end gap-2">
          <Button 
            variant="outline"
            onClick={() => window.open(empresa.receita_federal, '_blank')}
          >
            <ExternalLink className="h-4 w-4 mr-2" />
            Ver na Receita Federal
          </Button>
          <Button onClick={() => onOpenChange(false)}>
            Fechar
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default EmpresaDetailsDialog;
