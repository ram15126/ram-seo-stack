# Script Index

Auto-generated from each script's `--help`. **Calling conventions are not
uniform** — some scripts take a positional URL, others `--url`. Check the
usage column here before invoking, or run the script with `--help`.

Run from the repo root:

```bash
python "skills/seo/scripts/<script>" <args>
```

| Script | Usage | Purpose |
|---|---|---|
| `a11y_seo_checker.py` | `a11y_seo_checker.py [-h] [--timeout TIMEOUT] [--json] source` | Accessibility checks with direct SEO/UX impact. |
| `ai_crawler_policy_matrix.py` | `ai_crawler_policy_matrix.py [-h] [--path PATH] [--timeout TIMEOUT] [--json] site` | Compare robots.txt and llms.txt signals for AI crawlers. |
| `analyze_visual.py` | `analyze_visual.py [-h] [--timeout TIMEOUT] [--json] url` | Analyze visual aspects of a web page using Playwright. Usage: python analyze_visual.py https://example.com |
| `anchor_text_audit.py` | `anchor_text_audit.py [-h] [--depth DEPTH] [--max-pages MAX_PAGES] [--timeout TIMEOUT] [--json] url` | Audit internal anchor text quality and diversity. |
| `answer_block_scanner.py` | `answer_block_scanner.py [-h] [--timeout TIMEOUT] [--json] source` | Scan pages for answer-block and featured-snippet-ready formatting. |
| `article_seo.py` | `article_seo.py [-h] [--keyword KEYWORD] [--json] [--no-autocomplete] url` | Article SEO Optimizer & Keyword Researcher Fetches an article, detects the CMS (Blogger, WordPress, Ghost, gen |
| `audit_runner.py` | `audit_runner.py [-h] [--json JSON_OUTPUT] [--html HTML] [--markdown MARKDOWN] [--action-plan ACTION_PLAN] [--no-html] [--no-json] [--no-markdown] url` | Run the bundled SEO audit checks and write machine-readable plus report artifacts. This script reuses generate |
| `blog_inventory.py` | `blog_inventory.py [-h] [--path-contains PATH_CONTAINS]` | Build a blog inventory from a site_collect.py capture: topic clusters, hub detection, orphans, cannibalisation, duplicates. Reports coverage, never quality. |
| `brand_scanner.py` | `_(no argparse — read the file)_` | Brand Mention Scanner — Checks brand presence across AI-cited platforms. Brand mentions correlate 3x more stro |
| `broken_links.py` | `broken_links.py [-h] [--json] [--internal-only] [--workers WORKERS] [--timeout TIMEOUT] url` | Check for broken links on a web page. Crawls all links (internal + external) on a page, checks HTTP status. Re |
| `cache_compression_checker.py` | `cache_compression_checker.py [-h] [--include-assets] [--max-assets MAX_ASSETS] [--timeout TIMEOUT] [--json] source` | Check compression and caching headers for a page and optional assets. |
| `canonical_checker.py` | `canonical_checker.py [-h] [--url-file URL_FILE] [--check-targets] [--timeout TIMEOUT] [--json] [urls ...]` | Check canonical tags for self/cross-domain/chained targets. |
| `capture_screenshot.py` | `capture_screenshot.py [-h] [--output OUTPUT] [--viewport {desktop,laptop,tablet,mobile}] [--all] [--full] [--timeout TIMEOUT] url` | Capture screenshots of web pages using Playwright. Usage: python capture_screenshot.py https://example.com pyt |
| `citability_scorer.py` | `_(no argparse — read the file)_` | Citability Scorer — Analyzes content blocks for AI citation readiness. Scores passages based on how likely AI  |
| `citation_readiness.py` | `citation_readiness.py [-h] [--timeout TIMEOUT] [--json] source` | Assess citation and entity readiness for AI answers. |
| `collection_page_checker.py` | `collection_page_checker.py [-h] [--timeout TIMEOUT] [--json] source` | Check ecommerce collection/category pages for copy, filters, pagination, and crawlability. |
| `competitor_gap.py` | `competitor_gap.py [-h] --competitor COMPETITOR [--max-pages MAX_PAGES] [--json] url` | Competitor Topic Gap Analyzer Crawls competitor sitemaps / pages, extracts H-tag topics, and identifies conten |
| `content_decay_detector.py` | `content_decay_detector.py [-h] [--csv CSV_PATH] [--split-date SPLIT_DATE] [--decline-threshold DECLINE_THRESHOLD] [--min-impressions MIN_IMPRESSIONS] [--date-column DATE_COLUMN] [--url-column URL_COLUMN] [--query-column QUERY_COLUMN] [--clicks-column CLICKS_COLUMN] [--impressions-column IMPRESSIONS_COLUMN] [--position-column POSITION_COLUMN] [--json] [csv_file]` | Detect content decay and striking-distance keywords from CSV exports. |
| `content_intent_matcher.py` | `content_intent_matcher.py [-h] --keyword KEYWORD [--intent {commercial,informational,navigational,transactional}] [--timeout TIMEOUT] [--json] source` | Match page content to a target keyword and search intent. |
| `crawl_audit.py` | `crawl_audit.py [-h] [--max-pages MAX_PAGES] [--depth DEPTH] [--timeout TIMEOUT] [--no-sitemap] [--json] site` | Robots-aware shallow site crawler with SEO metadata checks. |
| `critical_request_chain.py` | `critical_request_chain.py [-h] [--fetch-css] [--timeout TIMEOUT] [--json] source` | Identify critical request chains and render-blocking resources from HTML. |
| `duplicate_content.py` | `duplicate_content.py [-h] [--depth DEPTH] [--max-pages MAX_PAGES] [--threshold THRESHOLD] [--json] url` | Duplicate & Thin Content Detector Detects near-duplicate pages and thin content across a site using MinHash /  |
| `eeat_signal_checker.py` | `eeat_signal_checker.py [-h] [--timeout TIMEOUT] [--json] source` | Check E-E-A-T signals in HTML content. |
| `entity_checker.py` | `entity_checker.py [-h] [--entity ENTITY] [--kg-api-key KG_API_KEY] [--json] url` | Entity SEO Checker Validates entity presence across Knowledge Graph signals: Wikidata, Wikipedia, sameAs prope |
| `external_link_quality.py` | `external_link_quality.py [-h] [--url-file URL_FILE] [--no-check-status] [--max-links MAX_LINKS] [--timeout TIMEOUT] [--json] [url]` | Audit external links for status, redirects, rel attributes, and trust patterns. |
| `faceted_nav_audit.py` | `faceted_nav_audit.py [-h] [--url-file URL_FILE] [--fetch] [--timeout TIMEOUT] [--json] [urls ...]` | Detect faceted navigation crawl traps from URLs and optional page fetches. |
| `fetch_page.py` | `fetch_page.py [-h] [--output OUTPUT] [--timeout TIMEOUT] [--no-redirects] url` | Fetch a web page with proper headers and error handling. Usage: python fetch_page.py https://example.com pytho |
| `finding_verifier.py` | `finding_verifier.py [-h] [--findings-json FINDINGS_JSON] [--context-json CONTEXT_JSON] [--json]` | Reusable finding verifier. Purpose: - remove duplicate findings across sources - suppress clearly contradicted |
| `font_audit.py` | `font_audit.py [-h] [--fetch-fonts] [--timeout TIMEOUT] [--json] source` | Audit font loading patterns that affect rendering and Core Web Vitals. |
| `freshness_checker.py` | `freshness_checker.py [-h] [--today TODAY] [--timeout TIMEOUT] [--json] source` | Check content freshness signals and stale references. |
| `generate_report.py` | `generate_report.py [-h] [--output OUTPUT] [--html HTML_OUTPUT] [--markdown MARKDOWN] [--action-plan ACTION_PLAN] [--no-html] [--no-markdown] url` | Generate an interactive HTML SEO report. Runs all analysis scripts and aggregates results into a single, self- |
| `gsc_checker.py` | `gsc_checker.py [-h] [--credentials CREDENTIALS] [--days DAYS] [--query QUERY] [--inspect INSPECT] [--json] site_url` | Google Search Console Data Checker Connects to the Google Search Console API (v3) to pull performance data, cr |
| `hreflang_checker.py` | `hreflang_checker.py [-h] [--json] [--verify-returns] url` | Hreflang Validator Validates hreflang implementations against all 8 checks defined in resources/skills/seo-hre |
| `hreflang_sitemap_validator.py` | `hreflang_sitemap_validator.py [-h] [--sitemap SITEMAP] [--timeout TIMEOUT] [--max-sitemaps MAX_SITEMAPS] [--json] site` | Validate hreflang annotations across sitemap indexes and sitemap URL sets. |
| `image_inventory.py` | `image_inventory.py [-h] [--fetch-images] [--timeout TIMEOUT] [--json] source` | Inventory images for SEO, accessibility, and performance signals. |
| `image_weight_audit.py` | `image_weight_audit.py [-h] [--fetch-images] [--timeout TIMEOUT] [--json] source` | Audit image weight, responsive image usage, and likely LCP image risk. |
| `indexability_matrix.py` | `indexability_matrix.py [-h] [--url-file URL_FILE] [--site SITE] [--timeout TIMEOUT] [--json] [urls ...]` | Build per-URL indexability verdicts. |
| `indexnow_checker.py` | `indexnow_checker.py [-h] --key KEY [--json] [--ping [PING ...]] [--ping-sitemap] [--engine {bing,yandex,seznam,naver}] url` | IndexNow Checker & Pinger Validates IndexNow implementation on a site and optionally pings the IndexNow API to |
| `info_gain_matrix.py` | `info_gain_matrix.py [-h] [--competitors [COMPETITORS ...]]` | Claim-level information-gain diff against pages that outrank you, with Core/Differentiator/Commodity/Opportunity gap classification. Does not fetch a SERP -- you supply competitor URLs in rank order. |
| `internal_links.py` | `internal_links.py [-h] [--depth DEPTH] [--max-pages MAX_PAGES] [--json] url` | Analyze internal link structure of a website. Checks link count, anchor text distribution, orphan page detecti |
| `javascript_render_audit.py` | `javascript_render_audit.py [-h] [--timeout TIMEOUT] [--render-timeout RENDER_TIMEOUT] [--json] source` | Compare raw HTML against rendered DOM SEO elements when Playwright is available. |
| `keyword_merge.py` | `keyword_merge.py [-h] [--min-competitors MIN_COMPETITORS] [--drop-brand-terms] [--json] staging` | Merge, dedupe and tier competitor keyword candidates from the mining pipeline. No API keys, no network. Never emits search volume or KD -- nothing in it measures either; priority is a tier from named evidence. |
| `lcp_subparts.py` | `lcp_subparts.py [-h] [--lighthouse-json LIGHTHOUSE_JSON] [--timeout TIMEOUT] [--json] [source]` | Estimate LCP subparts from Lighthouse JSON or lightweight page evidence. |
| `lighthouse_runner.py` | `lighthouse_runner.py [-h] [--strategy {mobile,desktop}] [--category {performance,seo,accessibility,best-practices}] [--timeout TIMEOUT] [--json] source` | Run local Lighthouse when available and normalize key audit output. |
| `link_profile.py` | `link_profile.py [-h] [--max-pages MAX_PAGES] [--gsc-credentials GSC_CREDENTIALS] [--json] url` | Link Profile Analyzer Crawls a site to build an internal/external link graph, identifies orphan pages, calcula |
| `llms_txt_checker.py` | `llms_txt_checker.py [-h] [--json] url` | Check for llms.txt file and validate its format. llms.txt is a proposed standard for providing LLM-friendly si |
| `llms_txt_generator.py` | `llms_txt_generator.py [-h] [--url-file URL_FILE] [--title TITLE] [--description DESCRIPTION] [--fetch-titles] [--timeout TIMEOUT] [--json] site [urls ...]` | Generate an llms.txt draft from site metadata and priority URLs. |
| `llmstxt_generator.py` | `_(no argparse — read the file)_` | llms.txt Generator — Creates and validates llms.txt files for AI crawler guidance. The llms.txt standard is an |
| `local_seo_checker.py` | `local_seo_checker.py [-h] [--timeout TIMEOUT] [--json] source` | Check local SEO signals: NAP, LocalBusiness schema, GBP links, reviews, and maps. |
| `log_file_analyzer.py` | `log_file_analyzer.py [-h] [--max-lines MAX_LINES] [--json] log_files [log_files ...]` | Analyze server logs for crawl budget and bot status-code patterns. |
| `mangools_keywords.py` | `mangools_keywords.py {locations,keywords,related} ... [--location LOCATION] [--json]` | **Live data — needs `MANGOOLS_API_TOKEN`.** Search volume, keyword difficulty (0-100) and 12-month volume trend from Mangools KWFinder. `keywords` scores a specific set (max 700), `related` finds ideas from a seed, `locations` resolves a location id. Reports missing data as null, never as zero. KD is link-based and understates local-pack competition. |
| `mobile_render_checker.py` | `mobile_render_checker.py [-h] [--render] [--timeout TIMEOUT] [--json] source` | Check mobile rendering risks with static HTML plus optional Playwright signals. |
| `orphan_pages_from_sitemap.py` | `orphan_pages_from_sitemap.py [-h] [--sitemap SITEMAP] [--depth DEPTH] [--max-pages MAX_PAGES] [--timeout TIMEOUT] [--json] site` | Find sitemap URLs that are not reachable from an internal crawl. |
| `pagespeed.py` | `pagespeed.py [-h] [--strategy {mobile,desktop,both}] [--json] [--api-key API_KEY] url` | Fetch Core Web Vitals and performance data from Google PageSpeed Insights API. Uses the free PSI API v5. An AP |
| `preflight_audit.py` | `preflight_audit.py [-h] [--timeout TIMEOUT] [--check-links] [--json]` | Run the blog pre-flight gate (SOP section 6) against a published page: answer block, key-fact openers, FAQ schema diffed against visible text, indexability, snippet eligibility, byline, links. |
| `product_schema_checker.py` | `product_schema_checker.py [-h] [--timeout TIMEOUT] [--json] source` | Check Product and ProductGroup JSON-LD for ecommerce rich-result readiness. |
| `readability.py` | `readability.py [-h] [--url URL] [--text TEXT] [--json] [file]` | Content readability analysis — pure Python, no external NLP dependencies. Computes Flesch-Kincaid Reading Ease |
| `redirect_backlink_reclaim.py` | `redirect_backlink_reclaim.py [-h] [--source-column SOURCE_COLUMN] [--target-column TARGET_COLUMN] [--max-rows MAX_ROWS] [--long-chain-threshold LONG_CHAIN_THRESHOLD] [--timeout TIMEOUT] [--json] csv_file` | Find backlink reclaim opportunities from a backlink export. |
| `redirect_checker.py` | `redirect_checker.py [-h] [--json] urls [urls ...]` | Check redirect chains for a URL. Follows the full redirect chain, reports each hop (status + destination), det |
| `review_schema_checker.py` | `review_schema_checker.py [-h] [--timeout TIMEOUT] [--json] source` | Check Review and AggregateRating markup for policy and misuse risks. |
| `rich_results_guard.py` | `rich_results_guard.py [-h] [--timeout TIMEOUT] [--json] source` | Guardrail checks for rich-result eligibility and retired schema types. |
| `robots_checker.py` | `robots_checker.py [-h] [--json] url` | Parse and analyze robots.txt for SEO and AI crawler management. Usage: python robots_checker.py https://exampl |
| `robots_path_tester.py` | `robots_path_tester.py [-h] [--agent AGENT] [--timeout TIMEOUT] [--json] site paths [paths ...]` | Test URL paths against robots.txt for multiple crawlers. |
| `schema_diff.py` | `schema_diff.py [-h] --type SCHEMA_TYPE [--timeout TIMEOUT] [--json] source` | Compare existing JSON-LD against a recommended bundled schema template. |
| `schema_required_props.py` | `schema_required_props.py [-h] [--type SCHEMA_TYPE] [--timeout TIMEOUT] [--json] source` | Validate required and recommended Schema.org properties in JSON-LD. |
| `schema_template_generator.py` | `schema_template_generator.py [-h] [--type SCHEMA_TYPE] [--detect-from DETECT_FROM] [--list] [--compact] [--timeout TIMEOUT] [--json]` | Generate JSON-LD templates from bundled schema templates. |
| `security_headers.py` | `security_headers.py [-h] [--json] url` | Check security headers relevant to SEO trust signals. Validates HTTPS, HSTS, CSP, X-Frame-Options, X-Content-T |
| `sitemap_checker.py` | `sitemap_checker.py [-h] [--sitemap SITEMAP] [--fetch-urls] [--max-urls MAX_URLS] [--timeout TIMEOUT] [--json] site` | Discover and validate XML sitemaps. |
| `sitemap_generator.py` | `sitemap_generator.py [-h] [--input INPUT] [--index] [--lastmod-today] [--json]` | Generate sitemap XML or sitemap indexes from URL manifests. |
| `slop_markers.py` | `slop_markers.py [-h] [--timeout TIMEOUT] [--json] source` | Report measurable AI-writing markers (vocabulary drift, sentence rhythm, copula ratio, leaked model markup, lexical richness). Evidence only -- never an authorship verdict. |
| `social_meta.py` | `social_meta.py [-h] [--json] url` | Validate Open Graph and Twitter Card meta tags. Checks og:title, og:description, og:image, og:url, twitter:car |
| `third_party_script_audit.py` | `third_party_script_audit.py [-h] [--fetch-scripts] [--timeout TIMEOUT] [--json] source` | Audit third-party scripts and blocking JavaScript tags. |
| `topical_cluster_mapper.py` | `topical_cluster_mapper.py [-h] [--csv CSV_PATH] [--timeout TIMEOUT] [--json] [sources ...]` | Map topical clusters and internal-link coverage from URLs, HTML, or CSV. |
| `url_quality.py` | `url_quality.py [-h] [--url-file URL_FILE] [--json] [urls ...]` | Analyze URL hygiene and variant risks. |
| `validate_schema.py` | `_(no argparse — read the file)_` | Post-edit schema validation helper. Validates JSON-LD schema after file edits. Returns exit code 2 to block if |
| `video_schema_checker.py` | `video_schema_checker.py [-h] [--timeout TIMEOUT] [--json] source` | Check VideoObject JSON-LD for video rich-result readiness. |
| `visual_regression_snapshot.py` | `visual_regression_snapshot.py [-h] [--url URL] [--output-dir OUTPUT_DIR] [--viewport {desktop,tablet,mobile}] [--all] [--full-page] [--timeout TIMEOUT] [--baseline BASELINE] [--current CURRENT] [--json]` | Create or compare visual regression snapshots. |
| `x_robots_header_checker.py` | `x_robots_header_checker.py [-h] [--url-file URL_FILE] [--timeout TIMEOUT] [--json] [urls ...]` | Inspect X-Robots-Tag headers. |
