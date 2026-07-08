## DataGuard user-study mixed-effects models (preferred analysis path).
##
## Run after data collection:
##   Rscript analysis/mixed_effects.R data/processed/trials.csv \
##                                    data/processed/tlx.csv \
##                                    analysis/results/
##
## Dependencies: lme4, lmerTest, emmeans, broom.mixed.

suppressPackageStartupMessages({
  library(lme4); library(lmerTest); library(emmeans); library(broom.mixed)
  library(dplyr); library(readr); library(tidyr)
})

args <- commandArgs(trailingOnly = TRUE)
trials_path <- args[1]
tlx_path    <- args[2]
out_dir     <- args[3]
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

trials <- read_csv(trials_path, show_col_types = FALSE) %>%
  mutate(condition = factor(condition, levels = c("C0","C1","C2")),
         stratum   = factor(stratum,   levels = c("S1","S2","S3")),
         pid       = factor(pid),
         app_id    = factor(app_id))

# ---- Long-format axis-level accuracy (4 rows per trial) ----
acc_long <- trials %>%
  pivot_longer(cols = starts_with("acc_"),
               names_to = "axis", values_to = "correct") %>%
  filter(!is.na(correct))

## -------------------- H1: accuracy --------------------
cat("=== H1: accuracy ~ condition + (1|pid) + (1|app_id) ===\n")
m_acc <- glmer(correct ~ condition + (1|pid) + (1|app_id),
               family = binomial(), data = acc_long,
               control = glmerControl(optimizer = "bobyqa"))
print(summary(m_acc))

em_acc <- emmeans(m_acc, ~ condition, type = "response")
write_csv(as_tibble(em_acc), file.path(out_dir, "h1_emmeans.csv"))
write_csv(as_tibble(pairs(em_acc, adjust = "holm")),
          file.path(out_dir, "h1_contrasts.csv"))

## -------------------- H4: interaction --------------------
cat("=== H4: accuracy ~ condition * stratum + (1|pid) + (1|app_id) ===\n")
m_int <- glmer(correct ~ condition * stratum + (1|pid) + (1|app_id),
               family = binomial(), data = acc_long,
               control = glmerControl(optimizer = "bobyqa"))
print(summary(m_int))
em_int <- emmeans(m_int, ~ condition | stratum, type = "response")
write_csv(as_tibble(em_int), file.path(out_dir, "h4_emmeans.csv"))
write_csv(as_tibble(pairs(em_int, adjust = "holm")),
          file.path(out_dir, "h4_contrasts.csv"))

## -------------------- H2: workload --------------------
cat("=== H2: tlx_global ~ condition + (1|pid) ===\n")
tlx <- read_csv(tlx_path, show_col_types = FALSE) %>%
  mutate(condition = factor(condition, levels = c("C0","C1","C2")),
         pid       = factor(pid))
m_tlx <- lmer(tlx_global ~ condition + (1|pid), data = tlx)
print(summary(m_tlx))
em_tlx <- emmeans(m_tlx, ~ condition)
write_csv(as_tibble(em_tlx), file.path(out_dir, "h2_emmeans.csv"))
write_csv(as_tibble(pairs(em_tlx, adjust = "holm")),
          file.path(out_dir, "h2_contrasts.csv"))

## -------------------- Time (secondary) ---------------
cat("=== Secondary: log(rt) ~ condition + (1|pid) + (1|app_id) ===\n")
trials$rt_log <- log(trials$rt_ms)
m_rt <- lmer(rt_log ~ condition + (1|pid) + (1|app_id),
             data = trials %>% filter(is.finite(rt_log)))
print(summary(m_rt))
em_rt <- emmeans(m_rt, ~ condition)
write_csv(as_tibble(em_rt), file.path(out_dir, "rt_emmeans.csv"))
write_csv(as_tibble(pairs(em_rt, adjust = "holm")),
          file.path(out_dir, "rt_contrasts.csv"))

cat("All models fitted. Results written to ", out_dir, "\n")
