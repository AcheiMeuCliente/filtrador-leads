import React, { useState, useEffect } from 'react';
import { Building2, Database, Loader2, Menu } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import FilterSidebar from '@/components/FilterSidebar';
import EmpresasTable from '@/components/EmpresasTable';
import { Empresa, ActiveFilters, FilterOptions } from '@/types/empresa';
import { useToast } from '@/hooks/use-toast';
import { apiService } from '@/services/apiService';
import { FilterSummaryResponse } from '@/types/empresa';
import ViewToggle from '@/components/ViewToggle';
import EmpresasCardView from '@/components/EmpresasCardView';
import EmpresaDetailsDialog from '@/components/EmpresaDetailsDialog';
import LeadAnalysisDialog from '@/components/LeadAnalysisDialog';

type ViewMode = 'table' | 'cards';

const Index = () => {
  const { toast } = useToast();
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;
  const [empresas, setEmpresas] = useState<Empresa[]>([]);
  const [totalEmpresas, setTotalEmpresas] = useState(0);
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<ViewMode>('table');
  const [selectedEmpresa, setSelectedEmpresa] = useState<Empresa | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [analysisOpen, setAnalysisOpen] = useState(false);
  const [mobileFiltersOpen, setMobileFiltersOpen] = useState(false);

  // Estado dos filtros
  const [activeFilters, setActiveFilters] = useState<ActiveFilters>({
    situacao: [],
    cnae_principal_codigo: [],
    cnae_principal_nome: [],
    cnae_secundario_codigo: [],
    cnae_secundario_nome: [],
    porte: [],
    tipo: [],
    matriz_filial: undefined,
    estado: [],
    municipio: [],
    bairro: [],
    descricao_natureza_juridica: [],
    descricao_motivo: [],
    dominio_corporativo: [],
    mei: undefined,
    simples: undefined,
    busca: '',
    capital_social_min: undefined,
    capital_social_max: undefined,
    data_inicio_min: undefined,
    data_inicio_max: undefined
  });

  // Estado das opções de filtro
  const [filterSummary, setFilterSummary] = useState<FilterSummaryResponse>({
    situacao: [],
    porte: [],
    tipo: [],
    estado: [],
    municipio: [],
    matriz_filial: [],
    descricao_natureza_juridica: [],
    cnae_principal_codigo: [],
    cnae_principal_nome: [],
    cnae_secundario_codigo: [],
    cnae_secundario_nome: [],
    descricao_motivo: [],
    dominio_corporativo: [],
    bairro: [],
    mei: [],
    simples: [],
    tem_email: [],
    tem_telefone: []
  });

  // Estado das opções de filtro legado (necessário para compatibilidade)
  const [filterOptions, setFilterOptions] = useState<FilterOptions>({
    situacao: [],
    cnae_principal: [],
    porte: [],
    tipo: [],
    matriz_filial: [],
    estado: [],
    municipio: [],
    bairro: [],
    descricao_natureza_juridica: [],
    mei: [],
    simples: []
  });

  // Estado das estatísticas
  const [stats, setStats] = useState({
    total: 0,
    totalGeral: 0,
    comTelefone: 0,
    comEmail: 0,
    idadeMedia: 0
  });

  // Carrega dados iniciais
  useEffect(() => {
    loadInitialData();
    const savedView = localStorage.getItem('preferredView') as ViewMode;
    if (savedView && ['table', 'cards'].includes(savedView)) {
      setViewMode(savedView);
    }
  }, []);

  // Carrega opções de filtro quando filtros mudam
  useEffect(() => {
    const debounceTimer = setTimeout(() => {
      loadFilterSummary();
    }, 300);

    return () => clearTimeout(debounceTimer);
  }, [activeFilters]);

  // Carrega empresas quando filtros mudam
  useEffect(() => {
    console.log('[Index] useEffect triggered by activeFilters:', activeFilters);
    const debounceTimer = setTimeout(() => {
      loadEmpresas();
    }, 300);

    return () => clearTimeout(debounceTimer);
  }, [activeFilters, currentPage]);

  // Função para carregar dados iniciais
  const loadInitialData = async () => {
    try {
      setLoading(true);
      // Ensure API service is ready (e.g. manifest loaded)
      await apiService.healthCheck();
      
      await loadFilterSummary();
      const statsResponse = await apiService.getStats();
      setStats(statsResponse);
    } catch (error) {
      console.error('Erro ao carregar dados iniciais:', error);
      toast({
        title: "Erro de Conexão",
        description: "Não foi possível carregar os dados iniciais. Verifique sua conexão.",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  // Função para carregar opções de filtro
  const loadFilterSummary = async () => {
    try {
      const summaryResponse = await apiService.getFilterSummary(activeFilters);
      setFilterSummary(summaryResponse);
    } catch (error) {
      console.error('Erro ao carregar opções de filtro:', error);
      toast({
        title: "Erro",
        description: "Não foi possível carregar as opções de filtro.",
        variant: "destructive"
      });
    }
  };

  // Função para carregar empresas
  const loadEmpresas = async () => {
    console.log('[Index] loadEmpresas called with filters:', activeFilters);
    try {
      setLoading(true);
      const response = await apiService.getEmpresas({
        page: currentPage,
        limit: itemsPerPage,
        search: activeFilters.busca || undefined,
        filters: activeFilters
      });

      if (currentPage === 1) {
        setEmpresas(response.data);
      } else {
        setEmpresas(prev => [...prev, ...response.data]);
      }
      setTotalEmpresas(response.pagination.totalItems);

      // Only update stats if filters changed, to avoid double calculation on pagination
      // But for now, keeping it simple to ensure consistency
      const statsResponse = await apiService.getStats(activeFilters);
      setStats(statsResponse);
    } catch (error) {
      console.error('Erro ao carregar empresas:', error);
      toast({
        title: "Erro ao buscar dados",
        description: "Não foi possível carregar a lista de empresas. Tente novamente.",
        variant: "destructive"
      });
      setEmpresas([]);
      setTotalEmpresas(0);
    } finally {
      setLoading(false);
    }
  };

  // Função para atualizar filtros
  const handleFiltersChange = (newFilters: ActiveFilters) => {
    setActiveFilters(newFilters);
    setCurrentPage(1); // Reset página ao mudar filtros
  };

  // Função para salvar filtros
  const handleSaveFilters = () => {
    localStorage.setItem('currentFilters', JSON.stringify(activeFilters));
    toast({
      title: "Filtros salvos",
      description: `${totalEmpresas} empresas encontradas com os filtros atuais.`,
    });
  };

  // Função para resetar filtros
  const handleResetFilters = () => {
    setActiveFilters({
      situacao: [],
      cnae_principal_codigo: [],
      cnae_principal_nome: [],
      cnae_secundario_codigo: [],
      cnae_secundario_nome: [],
      porte: [],
      tipo: [],
      matriz_filial: undefined,
      estado: [],
      municipio: [],
      bairro: [],
      descricao_natureza_juridica: [],
      descricao_motivo: [],
      dominio_corporativo: [],
      mei: undefined,
      simples: undefined,
      busca: '',
      capital_social_min: undefined,
      capital_social_max: undefined,
      data_inicio_min: undefined,
      data_inicio_max: undefined
    });
    toast({
      title: "Filtros resetados",
      description: "Todos os filtros foram limpos.",
    });
  };

  // Função para exportar resultados
  const handleExportResults = () => {
    if (empresas.length === 0) {
      toast({
        title: "Nenhum dado para exportar",
        description: "Não há empresas para exportar com os filtros atuais.",
        variant: "destructive"
      });
      return;
    }

    // Simular exportação
    const csvContent = [
      Object.keys(empresas[0] || {}).join(','),
      ...empresas.map(empresa => 
        Object.values(empresa).map(value => 
          typeof value === 'string' && value.includes(',') ? `"${value}"` : String(value || '')
        ).join(',')
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `empresas_filtradas_${new Date().toISOString().split('T')[0]}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    toast({
      title: "Exportação concluída",
      description: `${empresas.length} empresas exportadas com sucesso.`,
    });
  };

  // Funções de visualização
  const handleViewChange = (mode: ViewMode) => {
    setViewMode(mode);
    localStorage.setItem('preferredView', mode);
  };

  const handleViewDetails = (empresa: Empresa) => {
    setSelectedEmpresa(empresa);
    setDetailsOpen(true);
  };

  const handleViewAnalysis = (empresa: Empresa) => {
    setSelectedEmpresa(empresa);
    setAnalysisOpen(true);
  };

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Sidebar Desktop */}
      <div className="hidden md:block w-80 h-full border-r">
        <FilterSidebar
          filterOptions={filterOptions}
          filterSummary={filterSummary}
          activeFilters={activeFilters}
          onFiltersChange={handleFiltersChange}
          onSaveFilters={handleSaveFilters}
          onResetFilters={handleResetFilters}
          onExportResults={handleExportResults}
          resultsCount={totalEmpresas}
          className="h-full border-none"
        />
      </div>

      {/* Main Content */}
      <main className="flex-1 w-full h-full overflow-y-auto p-4 md:p-8 space-y-6">
          {/* Header Mobile & Title */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div className="flex items-center gap-2">
              <Sheet open={mobileFiltersOpen} onOpenChange={setMobileFiltersOpen}>
                <SheetTrigger asChild>
                  <Button variant="outline" size="icon" className="md:hidden">
                    <Menu className="h-4 w-4" />
                  </Button>
                </SheetTrigger>
                <SheetContent side="left" className="p-0 w-80">
                  <FilterSidebar
                    filterOptions={filterOptions}
                    filterSummary={filterSummary}
                    activeFilters={activeFilters}
                    onFiltersChange={handleFiltersChange}
                    onSaveFilters={() => {
                      handleSaveFilters();
                      setMobileFiltersOpen(false);
                    }}
                    onResetFilters={handleResetFilters}
                    onExportResults={handleExportResults}
                    resultsCount={totalEmpresas}
                    className="h-full border-none"
                    onClose={() => setMobileFiltersOpen(false)}
                    isOpen={mobileFiltersOpen}
                  />
                </SheetContent>
              </Sheet>
              <h1 className="text-2xl font-bold">Dashboard de Empresas</h1>
            </div>
            
            <div className="flex items-center gap-4">
              <ViewToggle
                viewMode={viewMode}
                onViewChange={handleViewChange}
              />
            </div>
          </div>

          {/* Estatísticas */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Total de Empresas</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.total}</div>
                <p className="text-xs text-muted-foreground">de {stats.totalGeral} no total</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Com Telefone</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.comTelefone}</div>
                <p className="text-xs text-muted-foreground">empresas com contato</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Com E-mail</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.comEmail}</div>
                <p className="text-xs text-muted-foreground">empresas com e-mail</p>
              </CardContent>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Idade Média</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{stats.idadeMedia.toFixed(1)}</div>
                <p className="text-xs text-muted-foreground">anos de atividade</p>
              </CardContent>
            </Card>
          </div>

          {/* Tabela/Cards de Empresas */}
          {loading && empresas.length === 0 ? (
            <div className="flex justify-center items-center p-8">
              <Loader2 className="h-8 w-8 animate-spin" />
            </div>
          ) : viewMode === 'table' ? (
            <EmpresasTable
              empresas={empresas}
              isLoading={loading}
              onEndReached={() => {
                if (!loading && empresas.length < totalEmpresas) {
                  setCurrentPage(prev => prev + 1);
                }
              }}
            />
          ) : (
            <EmpresasCardView
              empresas={empresas}
              currentPage={currentPage}
              itemsPerPage={itemsPerPage}
              onPageChange={setCurrentPage}
              onViewDetails={handleViewDetails}
              onViewAnalysis={handleViewAnalysis}
            />
          )}
      </main>

      {/* Modais */}
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
    </div>
  );
};

export default Index;
