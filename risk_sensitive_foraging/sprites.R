rm(list=ls(all=TRUE))
library(data.table)
extrafont::font_import(pattern = 'Roboto Slab Light')
extrafont::loadfonts(device = "win")
extrafont::fonttable()

fntbl <- fread(system.file("fontmap", "fonttable.csv", package="extrafontdb"))
fntbl[FullName == 'Roboto Slab Thin', FamilyName := 'Roboto Slab Thin']
fwrite(fntbl, system.file("fontmap", "fonttable.csv", package="extrafontdb"))

library(ggplot2)
library(scales)

make_sprites()

make_sprites <- function() {
  d <- fread('environment.csv', drop='budget')
  dc <- fread('critical_trials.csv', drop = c('budget', 'state', 'trial'))
  setnames(dc, names(d))
  d <- rbind(d, dc)

  d1 <- d[,1:(1/2*ncol(d)),]
  d2 <- d[, (1/2*ncol(d)+1):ncol(d),]
  setnames(d2, names(d1))
  d <- rbind(d1,d2, fill = T)
  d <- unique(d)

  for (i in 1:nrow(d)) {
    dd <- d[i]
    dd[, id := 1:.N]
    dd <- melt(dd, id = 'id', measure = list(1:2, 3:4), value = c('x','p'))
    dd[, variablef := factor(x, levels = x, labels = paste0('+', x))]
    dd[, variablef2 := reorder(variablef, 2:1)]
    plot_and_save(dd, 'variablef2', 1:2)
    plot_and_save(dd, 'variablef2', 2:1)
  }
}




plot_and_save <- function(dd, v, colorder) {
  cols <- c('grey85', 'grey50')
  cols <- cols[colorder]
  leg.l.margin <- ifelse(dd[, max(x)] >= 10, .22, .25)
  leg.txt.r.margin <- ifelse(dd[, max(x)] >= 10, .6, .8)

    p <- ggplot(dd, aes_string(x = 0, fill = v, color = v, group = v)) +
      geom_bar(aes(y = p), stat = 'identity', width = .2, color = NA) +
      theme_void(base_family = 'Roboto Slab Thin', base_size = 30) +
      coord_flip() +
      xlim(-.2,1) +
      geom_point(aes(x = -100, y = p), size = .5) +
      theme(
        legend.direction = 'horizontal',
        legend.position = c(0,.5),
        legend.justification = c(0, 0),
        legend.key.width = unit(.2, 'lines'),
        legend.key.height = unit(.01, 'lines'),
        legend.title = element_blank(),
        legend.margin = margin(l = leg.l.margin, r = .05, unit = 'npc'),
        legend.text = element_text(
          size = 4,
          margin = margin(r = leg.txt.r.margin, l = .31, unit = "npc")),
        aspect.ratio = 1/1.6,
        plot.margin = margin(0)) +
      scale_fill_manual(values = cols) +
      scale_color_manual(values = cols) +
      guides(fill = 'none', color = guide_legend(reverse = TRUE,
        override.aes = list(shape = 16))) +
      geom_text( aes(y = p, label = percent(p, accuracy = 1)),
        position = position_stack(vjust = .5),
        size = .6,
        family = 'Roboto Slab',
        color = 'black')

  fn <- dd[order(variablef), paste(x,p*100,collapse='_',sep='_')]
  fn <- paste0('sprite_', fn, '_minprisdark', colorder[1]-1, '.png')
  ggsave(plot = p, file = file.path('static', 'risk_sensitive_foraging', 'sprites', fn), w = .5, h = .5/1.6, units='in', dpi = 600)
}